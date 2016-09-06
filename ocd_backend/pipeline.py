from datetime import datetime
from uuid import uuid4

from elasticsearch.exceptions import NotFoundError
from celery import chain

from ocd_backend.es import elasticsearch as es
from ocd_backend import settings, celery_app
from ocd_backend.log import get_source_logger
from ocd_backend.utils.misc import load_object
from ocd_backend.exceptions import ConfigurationError

logger = get_source_logger('pipeline')


def get_alias_for_source(source_definition):
    return '{prefix}_{index_name}'.format(
        prefix=settings.DEFAULT_INDEX_PREFIX,
        index_name=source_definition.get(
            'index_name', source_definition.get('id')))

def get_timed_index_name_for_alias(index_alias,index_date=datetime.utcnow()):
    return '{index_alias}_{now}'.format(
        index_alias=index_alias, now=index_date.strftime('%Y%m%d%H%M%S'))

def initialize_index(source_definition, current_date_and_time):
    # index_name is an alias of the current version of the index
    index_alias = get_alias_for_source(source_definition)

    # initialize an index if it does not exist yet
    if not es.indices.exists(index_alias):
        index_name = get_timed_index_name_for_alias(
            index_alias, current_date_and_time)

        es.indices.create(index_name)
        es.indices.put_alias(name=index_alias, index=index_name)

    # disable index refresh
    if source_definition['keep_index_on_update']:
        es.indices.put_settings(index=index_name, body={"index" : {"refresh_interval" : "-1"}})

    return index_alias

def get_current_index(index_alias):
    # Find the current index name behind the alias specified in the config
    try:
        current_index_aliases = es.indices.get_alias(name=index_alias)
    except NotFoundError:
        raise ConfigurationError('Index with alias "{index_alias}" does '
                                 'not exist'.format(index_alias=index_alias))

    return current_index_aliases.keys()[0]

def get_new_index(source_definition, current_index_name, index_alias, current_date_and_time):
    # Check if the source specifies that any update should be added to
    # the current index instead of a new one
    if source_definition['keep_index_on_update']:
        return current_index_name
    else:
        return '{index_alias}_{now}'.format(
            index_alias=index_alias,
            now=current_date_and_time.strftime('%Y%m%d%H%M%S'))

def setup_pipeline(source_definition):
    current_date_and_time = datetime.utcnow()

    # first thhe secondary index
    index_alias = initialize_index(source_definition, current_date_and_time)
    current_index_name = get_current_index(index_alias)
    new_index_name = get_new_index(
        source_definition, current_index_name, index_alias, current_date_and_time)

    # now the combined index
    combined_source_definition = {
        'id': 'test_source',
        'index_name': 'combined_index',
        'keep_index_on_update': source_definition['keep_index_on_update']
    }
    initialize_index(combined_source_definition, current_date_and_time)
    current_combined_index_name = get_current_index(settings.COMBINED_INDEX)
    new_combined_index_name = get_new_index(
        combined_source_definition, current_combined_index_name,
        settings.COMBINED_INDEX, current_date_and_time)

    # now load objects and prepare the run ...
    extractor = load_object(source_definition['extractor'])(source_definition)
    transformer = load_object(source_definition['transformer'])()
    enrichers = [(load_object(enricher[0])(), enricher[1]) for enricher in
                 source_definition['enrichers']]
    loader = load_object(source_definition['loader'])()

    # Parameters that are passed to each task in the chain
    params = {
        'run_identifier': 'pipeline_{}'.format(uuid4().hex),
        'current_index_name': current_index_name,
        'new_index_name': new_index_name,
        'index_alias': index_alias,
        'current_combined_index_name': current_combined_index_name,
        'new_combined_index_name': new_combined_index_name
    }

    celery_app.backend.set(params['run_identifier'], 'running')
    run_identifier_chains = '{}_chains'.format(params['run_identifier'])

    try:
        for item in extractor.run():
            # Generate an identifier for each chain, and record that in
            # {}_chains, so that we can know for sure when all tasks
            # from an extractor have finished
            params['chain_id'] = uuid4().hex
            celery_app.backend.add_value_to_set(set_name=run_identifier_chains,
                                                value=params['chain_id'])

            item_chain = chain()

            # Tranform
            item_chain |= transformer.s(
                *item,
                source_definition=source_definition,
                **params
            )

            # Enrich
            for enricher_task, enricher_settings in enrichers:
                item_chain |= enricher_task.s(
                    source_definition=source_definition,
                    enricher_settings=enricher_settings,
                    **params
                )

            # Load
            item_chain |= loader.s(
                source_definition=source_definition,
                **params
            )

            item_chain.delay()
    except:
        logger.error('An exception has occured in the "{extractor}" extractor. '
                     'Setting status of run identifier "{run_identifier}" to '
                     '"error".'
                     .format(index=new_index_name,
                             run_identifier=params['run_identifier'],
                             extractor=source_definition['extractor']))

        celery_app.backend.set(params['run_identifier'], 'error')
        raise

    celery_app.backend.set(params['run_identifier'], 'done')
