
from ocd_backend import celery_app
from ocd_backend import settings
from ocd_backend.es import elasticsearch as es
from ocd_backend.log import get_source_logger


log = get_source_logger('ocd_backend.tasks')


class BaseCleanup(celery_app.Task):
    ignore_result = True

    def run(self, *args, **kwargs):
        run_identifier = kwargs.get('run_identifier')
        run_identifier_chains = '{}_chains'.format(run_identifier)
        self._remove_chain(run_identifier_chains, kwargs.get('chain_id'))

        if self.backend.get_set_cardinality(run_identifier_chains) < 1 and self.backend.get(run_identifier) == 'done':
            self.backend.remove(run_identifier_chains)
            self.run_finished(**kwargs)
        else:
            # If the extractor is still running, extend the lifetime of the
            # identifier
            self.backend.update_ttl(run_identifier, settings.CELERY_CONFIG
                                    .get('CELERY_TASK_RESULT_EXPIRES', 1800))

    def _remove_chain(self, run_identifier, value):
        self.backend.remove_value_from_set(run_identifier, value)

    def run_finished(self, run_identifier, **kwargs):
        raise NotImplementedError('Cleanup is highly dependent on what you use '
                                  'for storage, so this should be implemented '
                                  'in a subclass.')


class CleanupElasticsearch(BaseCleanup):

    def run_finished(self, run_identifier, **kwargs):
        log.info('Cleaning up after finished run...')
        current_index_name = kwargs.get('current_index_name')
        new_index_name = kwargs.get('new_index_name')
        alias = kwargs.get('index_alias')
        additional_aliases = kwargs.get('index_aliases')
        current_index_names = kwargs.get('current_index_names')
        new_index_names = kwargs.get('new_index_names')
        alias_changes = zip(
            additional_aliases, current_index_names, new_index_names)
        log.info('Finished run {}. Removing alias "{}" from "{}", and '
                 'applying it to "{}"'.format(run_identifier, alias,
                                              current_index_name,
                                              new_index_name))

        for an_alias, a_current_name, a_new_name in alias_changes:
            log.info('Finished run {}. Removing alias "{}" from "{}", and '
                     'applying it to "{}"'.format(run_identifier, an_alias,
                                                  a_current_name,
                                                  a_new_name))

        # enable index refresh again
        #if source_definition['keep_index_on_update']:
        # es.indices.put_settings(index='%s,%s' % (
        #     new_index_name, ','.join(new_index_names),),
        #     body={"index" : {"refresh_interval" : "1s"}})


        actions = {
            'actions': [
                {
                    'remove': {
                        'index': current_index_name,
                        'alias': alias
                    }
                },
                {
                    'add': {
                        'index': new_index_name,
                        'alias': alias
                    }
                }
            ]
        }

        for an_alias, a_current_name, a_new_name in alias_changes:
            actions['actions'] += [
                {
                    'remove': {
                        'index': a_current_name,
                        'alias': an_alias
                    }
                },
                {
                    'add': {
                        'index': a_new_name,
                        'alias': an_alias
                    }
                }
            ]

        # Set alias to new index
        es.indices.update_aliases(body=actions)

        # Remove old index
        # FIXME: do we want to keep old indexes? If so how many?
        if current_index_name != new_index_name:
            es.indices.delete(index=current_index_name)
