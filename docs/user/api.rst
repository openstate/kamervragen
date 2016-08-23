.. _restapi:

RESTful API
===========

.. warning::

   This page currently shows a draft of the API specification. **The format of some of the request/response pairs is still subject to change!**

General notes
-------------

The API returns JSON data in all of its responses (unless stated otherwise). Standard HTTP response codes are used to indicate errors. In case of an error, a more detailed description can be found in the JSON response body. UTF-8 character encoding is used in the responses.

All API URLs referenced in this documentation start with the following base part:

    :rest_api_v0:`v0`

All API endpoints are designed according to the idea that there is an operation within a *context*: methods on the "root" context are executed across all datasets; :ref:`/search <rest_search>` executes across all data sources, whereas :ref:`/datasets/<dataset_name> <rest_source_search>` executes a search on a specific dataset.

Arguments to an endpoint are placed behind the method definition.
