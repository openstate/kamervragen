.. _restapi:

RESTful API
===========

General notes
-------------

The API returns data in the JSON-LD format for all of its responses (unless stated otherwise), which stands for `JSON for Linked Data <https://en.wikipedia.org/wiki/JSON-LD>`__. The difference is that these JSON-LD responses contain ``@context`` and ``@id`` keys. The ``@context`` key contains an object specifying all field names you will encounter in the results. Each field name key has a URI as value in order to give it a unique identifier; Note that these URIs look like URLs but they do not necessary resolve to a working website and if it does resolve to a working website then you will not find more information related to the linked data. You should just use these URIs as unique identifier for linked data purposes. The ``@id`` key contains a UTF-8 character encoding is used in the responses.

All API URLs referenced in this documentation start with the following base part:

    :rest_api_v0:`v0` (which by itself does not hold any data and instead will redirect you to this documentation)

All API calls make use of HTTP GET requests so you can easily explore the API in your browser. You might want to use a browser extension which formats the returned JSON in a more readable way (e.g., using JSONview for `Firefox <https://addons.mozilla.org/en-US/firefox/addon/jsonview/>`__ or `Chrome <https://chrome.google.com/webstore/detail/jsonview/chklaanhfefbnpoihckbnefhakgolnmc>`__).

Note that many datasets are very large and your browsers might have a hard time showing the data. We thus recommend to use a more lightweight way of retrieving and viewing the data, such as ``curl``.

Retrieve all datasets available in the API
------------------------------------------

.. http:get:: /search

   **Example request**

     https://api.duo.nl/v0/search

   **Example response** (formatted and limited to 3 results for readability)

    .. sourcecode:: http

      {
        "@context": {
          "results": "https://data.duo.nl/#results",
          "dataset_url": "https://api.duo.nl/docs/#dataset_url",
          "dataset_source": "https://api.duo.nl/docs/#dataset_source",
          "dataset_query": "https://api.duo.nl/docs/#dataset_query",
          "dataset_name": "https://api.duo.nl/docs/#dataset_name",
          "dataset_documentation": "https://api.duo.nl/docs/#dataset_documentation"
        },
        "@id": "https://api.duo.nl/v0/search",
        "results": [
          {
            "dataset_url": "https://api.duo.nl/v0/datasets/01.-hoofdvestigingen-basisonderwijs",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-basisonderwijs.csv",
            "dataset_name": "01.-hoofdvestigingen-basisonderwijs",
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/po/adressen/adressen_po_1.jsp"
          },
          {
            "dataset_url": "https://api.duo.nl/v0/datasets/02.-hoofdvestigingen-speciaal-%28basis%29onderwijs",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/02.-hoofdvestigingen-speciaal-(basis)onderwijs.csv",
            "dataset_name": "02.-hoofdvestigingen-speciaal-(basis)onderwijs",
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/po/adressen/adressen_po_2.jsp"
          },
          {
            "dataset_url": "https://api.duo.nl/v0/datasets/04.-alle-vestigingen-speciaal-%28basis%29onderwijs",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/04.-alle-vestigingen-speciaal-(basis)onderwijs.csv",
            "dataset_name": "04.-alle-vestigingen-speciaal-(basis)onderwijs",
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/po/adressen/adressen_po_4.jsp"
          },
          ...
        ]
      }

Search for datasets based on their name
---------------------------------------

.. http:get:: /search?dataset_name=(value)

   This API call let's you search for datasets based on their name. In the example below we find all datasets whose names contain the string ``hoofdvestigingen``.

   **Example request**

     https://api.duo.nl/v0/search?dataset_name=hoofdvestigingen

   **Example response** (formatted for readability)

    .. sourcecode:: http

      {
        "@context": {
          "results": "https://data.duo.nl/#results",
          "dataset_url": "https://api.duo.nl/docs/#dataset_url",
          "dataset_source": "https://api.duo.nl/docs/#dataset_source",
          "dataset_query": "https://api.duo.nl/docs/#dataset_query",
          "dataset_name": "https://api.duo.nl/docs/#dataset_name",
          "dataset_documentation": "https://api.duo.nl/docs/#dataset_documentation"
        },
        "@id": "https://api.duo.nl/v0/search?dataset_name=hoofdvestigingen",
        "results": [
          {
            "dataset_url": "https://api.duo.nl/v0/datasets/01.-hoofdvestigingen-basisonderwijs",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-basisonderwijs.csv",
            "dataset_name": "01.-hoofdvestigingen-basisonderwijs",
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/po/adressen/adressen_po_1.jsp"
          },
          {
            "dataset_url": "https://api.duo.nl/v0/datasets/01.-hoofdvestigingen-vo",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv",
            "dataset_name": "01.-hoofdvestigingen-vo",
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/vo/adressen/adressen_vo_1.jsp"
          },
          {
            "dataset_url": "https://api.duo.nl/v0/datasets/02.-hoofdvestigingen-speciaal-%28basis%29onderwijs",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/02.-hoofdvestigingen-speciaal-(basis)onderwijs.csv",
            "dataset_name": "02.-hoofdvestigingen-speciaal-(basis)onderwijs",
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/po/adressen/adressen_po_2.jsp"
          }
        ]
      }

Retrieve all datasets that contains a specific field name
---------------------------------------------------------

.. http:get:: /search?field_name=(field_name)

   Use this API call if you want to find all datasets that contain a specific field. In the example below we find all datasets which contain the field ``vestigingsnummer``.

   **Example request**

     https://api.duo.nl/v0/search?field_name=vestigingsnummer

   **Example response** (formatted and limited to 3 results for readability)

    .. sourcecode:: http

      {
        "@context": {
          "results": "https://data.duo.nl/#results",
          "dataset_url": "https://api.duo.nl/docs/#dataset_url",
          "dataset_source": "https://api.duo.nl/docs/#dataset_source",
          "dataset_query": "https://api.duo.nl/docs/#dataset_query",
          "dataset_name": "https://api.duo.nl/docs/#dataset_name",
          "dataset_documentation": "https://api.duo.nl/docs/#dataset_documentation"
        },
        "@id": "https://api.duo.nl/v0/search?field_name=vestigingsnummer",
        "results": [
          {
            "dataset_url": "https://api.duo.nl/v0/datasets/04.-alle-vestigingen-speciaal-%28basis%29onderwijs",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/04.-alle-vestigingen-speciaal-(basis)onderwijs.csv",
            "dataset_name": "04.-alle-vestigingen-speciaal-(basis)onderwijs",
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/po/adressen/adressen_po_4.jsp"
          },
          {
            "dataset_url": "https://api.duo.nl/v0/datasets/03.-alle-vestigingen-basisonderwijs",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/03.-alle-vestigingen-basisonderwijs.csv",
            "dataset_name": "03.-alle-vestigingen-basisonderwijs",
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/po/adressen/adressen_po_3.jsp"
          },
          {
            "dataset_url": "https://api.duo.nl/v0/datasets/09.-instellingen-per-samenwerkingsverband-passend-onderwijs-po",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/09.-instellingen-per-samenwerkingsverband-passend-onderwijs-po.csv",
            "dataset_name": "09.-instellingen-per-samenwerkingsverband-passend-onderwijs-po",
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/po/adressen/adressen_po_9.jsp"
          },
          ...
        ]
      }

Search all datasets on a specific field
---------------------------------------

.. http:get:: /search?(field_name)=(value)

   Use this API call to retrieve all datasets which contain a field with a specific value. Not all fields can be searched. The field names that can be searched are:

   * ``brin``
   * ``bevoegd_gezag``
   * ``instellingsnaam``
   * ``vestigingsnaam``
   * ``vestigingsnummer``
   * ``gemeentenummer``
   * ``gemeentenaam``
   * ``plaatsnaam``
   * ``provincie``

   Note that the actual field names for ``bevoegd_gezag`` are not standardized accross datasets. The field names in the datasets can be ``bevoegd_gezag``, ``bevoegd_gezag_nummer``, ``bevoegd_gezag_school`` or ``administratienummer``. This is not a problem when using this API call, because it does search all the different spellings of the ``bevoegd_gezag`` field in all datasets. Just be aware that the the field name might be different when you use the resulting datasets. The same holds for ``brin``. In the API call you use ``brin``, but all field names in the datasets are called ``brin_nummer``.

   In the example below we retrieve all datasets which have a ``brin`` field with the value ``00LY``.

   **Example request**

     https://api.duo.nl/v0/search?brin=00LY

   **Example response** (formatted and limited to 3 results for readability)

    .. sourcecode:: http

      {
        "@context": {
          "results": "https://data.duo.nl/#results",
          "dataset_url": "https://api.duo.nl/docs/#dataset_url",
          "dataset_source": "https://api.duo.nl/docs/#dataset_source",
          "dataset_query": "https://api.duo.nl/docs/#dataset_query",
          "dataset_name": "https://api.duo.nl/docs/#dataset_name",
          "dataset_documentation": "https://api.duo.nl/docs/#dataset_documentation"
        },
        "@id": "https://api.duo.nl/v0/search?brin=00LY",
        "results": [
          {
            "dataset_url": "https://api.duo.nl/v0/datasets/01.-hoofdvestigingen-vo",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv",
            "dataset_query": "https://api.duo.nl/v0/datasets/01.-hoofdvestigingen-vo/search?uni_brin=00LY",
            "dataset_name": "01.-hoofdvestigingen-vo",
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/vo/adressen/adressen_vo_1.jsp"
          },
          {
            "dataset_url": "https://api.duo.nl/v0/datasets/01.-leerlingen-vo-per-vestiging-naar-onderwijstype-2014-2015",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/01.-leerlingen-vo-per-vestiging-naar-onderwijstype-2014-2015.csv",
            "dataset_query": "https://api.duo.nl/v0/datasets/01.-leerlingen-vo-per-vestiging-naar-onderwijstype-2014-2015/search?uni_brin=00LY",
            "dataset_name": "01.-leerlingen-vo-per-vestiging-naar-onderwijstype-2014-2015",
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/vo/Leerlingen/leerlingen_vo_1.jsp"
          },
          {
            "dataset_url": "https://api.duo.nl/v0/datasets/01.-leerlingen-vo-per-vestiging-naar-onderwijstype-2013-2014",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/01.-leerlingen-vo-per-vestiging-naar-onderwijstype-2013-2014.csv",
            "dataset_query": "https://api.duo.nl/v0/datasets/01.-leerlingen-vo-per-vestiging-naar-onderwijstype-2013-2014/search?uni_brin=00LY",
            "dataset_name": "01.-leerlingen-vo-per-vestiging-naar-onderwijstype-2013-2014",
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/vo/Leerlingen/leerlingen_vo_1.jsp"
          },
          ...
        ]
      }

Show a single dataset
---------------------

.. http:get:: /datasets/(dataset_name)

   Show all records for a single dataset. The example request below retrieves all records for the dataset ``06.-bevoegde-gezagen-speciaal-(basis)onderwijs``.

   **Example request**

     https://api.duo.nl/v0/datasets/06.-bevoegde-gezagen-speciaal-(basis)onderwijs

   **Example response** (formatted and limited to 2 results for readability)

    .. sourcecode:: http

      {
        "@context": {
          "GEMEENTENUMMER": "https://www.duo.nl/open_onderwijsdata/images/06.-bevoegde-gezagen-speciaal-(basis)onderwijs.csv#GEMEENTENUMMER",
          "POSTCODE CORRESPONDENTIEADRES": "https://www.duo.nl/open_onderwijsdata/images/06.-bevoegde-gezagen-speciaal-(basis)onderwijs.csv#POSTCODE%20CORRESPONDENTIEADRES",
          "PLAATSNAAM CORRESPONDENTIEADRES": "https://www.duo.nl/open_onderwijsdata/images/06.-bevoegde-gezagen-speciaal-(basis)onderwijs.csv#PLAATSNAAM%20CORRESPONDENTIEADRES",
          "GEMEENTENAAM": "https://www.duo.nl/open_onderwijsdata/images/06.-bevoegde-gezagen-speciaal-(basis)onderwijs.csv#GEMEENTENAAM",
          "BEVOEGD GEZAG NUMMER": "https://www.duo.nl/open_onderwijsdata/images/06.-bevoegde-gezagen-speciaal-(basis)onderwijs.csv#BEVOEGD%20GEZAG%20NUMMER",
          "PLAATSNAAM": "https://www.duo.nl/open_onderwijsdata/images/06.-bevoegde-gezagen-speciaal-(basis)onderwijs.csv#PLAATSNAAM",
          "TELEFOONNUMMER": "https://www.duo.nl/open_onderwijsdata/images/06.-bevoegde-gezagen-speciaal-(basis)onderwijs.csv#TELEFOONNUMMER",
          "BEVOEGD GEZAG NAAM": "https://www.duo.nl/open_onderwijsdata/images/06.-bevoegde-gezagen-speciaal-(basis)onderwijs.csv#BEVOEGD%20GEZAG%20NAAM",
          "HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES": "https://www.duo.nl/open_onderwijsdata/images/06.-bevoegde-gezagen-speciaal-(basis)onderwijs.csv#HUISNUMMER-TOEVOEGING%20CORRESPONDENTIEADRES",
          "STRAATNAAM CORRESPONDENTIEADRES": "https://www.duo.nl/open_onderwijsdata/images/06.-bevoegde-gezagen-speciaal-(basis)onderwijs.csv#STRAATNAAM%20CORRESPONDENTIEADRES",
          "results": "https://data.duo.nl/#results",
          "DENOMINATIE": "https://www.duo.nl/open_onderwijsdata/images/06.-bevoegde-gezagen-speciaal-(basis)onderwijs.csv#DENOMINATIE",
          "SOORT PRIMAIR ONDERWIJS": "https://www.duo.nl/open_onderwijsdata/images/06.-bevoegde-gezagen-speciaal-(basis)onderwijs.csv#SOORT%20PRIMAIR%20ONDERWIJS",
          "STRAATNAAM": "https://www.duo.nl/open_onderwijsdata/images/06.-bevoegde-gezagen-speciaal-(basis)onderwijs.csv#STRAATNAAM",
          "HUISNUMMER-TOEVOEGING": "https://www.duo.nl/open_onderwijsdata/images/06.-bevoegde-gezagen-speciaal-(basis)onderwijs.csv#HUISNUMMER-TOEVOEGING",
          "POSTCODE": "https://www.duo.nl/open_onderwijsdata/images/06.-bevoegde-gezagen-speciaal-(basis)onderwijs.csv#POSTCODE",
          "ADMINISTRATIEKANTOORNUMMER": "https://www.duo.nl/open_onderwijsdata/images/06.-bevoegde-gezagen-speciaal-(basis)onderwijs.csv#ADMINISTRATIEKANTOORNUMMER",
          "INTERNETADRES": "https://www.duo.nl/open_onderwijsdata/images/06.-bevoegde-gezagen-speciaal-(basis)onderwijs.csv#INTERNETADRES"
        },
        "@id": "https://api.duo.nl/v0/datasets/06.-bevoegde-gezagen-speciaal-(basis)onderwijs",
        "results": [
          {
            "TELEFOONNUMMER": "          ",
            "SOORT PRIMAIR ONDERWIJS": "(V)SO",
            "PLAATSNAAM CORRESPONDENTIEADRES": "TILBURG",
            "GEMEENTENAAM": "TILBURG",
            "BEVOEGD GEZAG NUMMER": "20233",
            "PLAATSNAAM": "TILBURG",
            "BEVOEGD GEZAG NAAM": "Stichting Mytylschool Tilburg",
            "HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES": "5022",
            "STRAATNAAM CORRESPONDENTIEADRES": "Postbus",
            "DENOMINATIE": "Rooms-Katholiek",
            "GEMEENTENUMMER": "0855",
            "STRAATNAAM": "Professor Stoltehof",
            "HUISNUMMER-TOEVOEGING": "1",
            "POSTCODE": "5022 KE",
            "ADMINISTRATIEKANTOORNUMMER": "401",
            "INTERNETADRES": "                                                                                ",
            "POSTCODE CORRESPONDENTIEADRES": "5004 EA"
          },
          {
            "TELEFOONNUMMER": "0402902345",
            "SOORT PRIMAIR ONDERWIJS": "(V)SO",
            "PLAATSNAAM CORRESPONDENTIEADRES": "EINDHOVEN",
            "GEMEENTENAAM": "EINDHOVEN",
            "BEVOEGD GEZAG NUMMER": "21657",
            "PLAATSNAAM": "EINDHOVEN",
            "BEVOEGD GEZAG NAAM": "Stichting Vitus Zuid",
            "HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES": "1377",
            "STRAATNAAM CORRESPONDENTIEADRES": "Postbus",
            "DENOMINATIE": "Overige",
            "GEMEENTENUMMER": "0772",
            "STRAATNAAM": "Toledolaan",
            "HUISNUMMER-TOEVOEGING": "3",
            "POSTCODE": "5629 CC",
            "ADMINISTRATIEKANTOORNUMMER": "413",
            "INTERNETADRES": "www.vituszuid.nl",
            "POSTCODE CORRESPONDENTIEADRES": "5602 BJ"
          },
          ...
        ]
      }

Search a specific datasets on a specific field
----------------------------------------------

.. http:get:: /datasets/(dataset_name)/search?(field_name)=(value)

   See the details in the `Search all datasets on a specific field`_ section on which fields can be searched.

   In the example below we retrieve all records from dataset ``01.-hoofdvestigingen-vo`` where the ``brin`` field matches the value ``18BR``.

   **Example request**

     https://api.duo.nl/v0/datasets/01.-hoofdvestigingen-vo/search?brin=18BR

   **Example response** (formatted for readability)

    .. sourcecode:: http

      {
        "@context": {
          "TELEFOONNUMMER": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#TELEFOONNUMMER",
          "STRAATNAAM": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#STRAATNAAM",
          "COROPGEBIED CODE": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#COROPGEBIED%20CODE",
          "ONDERWIJSGEBIED CODE": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#ONDERWIJSGEBIED%20CODE",
          "HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#HUISNUMMER-TOEVOEGING%20CORRESPONDENTIEADRES",
          "INSTELLINGSNAAM": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#INSTELLINGSNAAM",
          "RPA-GEBIED CODE": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#RPA-GEBIED%20CODE",
          "HUISNUMMER-TOEVOEGING": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#HUISNUMMER-TOEVOEGING",
          "RMC-REGIO CODE": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#RMC-REGIO%20CODE",
          "WGR-GEBIED NAAM": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#WGR-GEBIED%20NAAM",
          "PROVINCIE": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#PROVINCIE",
          "INTERNETADRES": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#INTERNETADRES",
          "BEVOEGD GEZAG NUMMER": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#BEVOEGD%20GEZAG%20NUMMER",
          "NODAAL GEBIED CODE": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#NODAAL%20GEBIED%20CODE",
          "BRIN NUMMER": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#BRIN%20NUMMER",
          "POSTCODE": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#POSTCODE",
          "WGR-GEBIED CODE": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#WGR-GEBIED%20CODE",
          "RPA-GEBIED NAAM": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#RPA-GEBIED%20NAAM",
          "RMC-REGIO NAAM": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#RMC-REGIO%20NAAM",
          "results": "https://data.duo.nl/#results",
          "GEMEENTENAAM": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#GEMEENTENAAM",
          "NODAAL GEBIED NAAM": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#NODAAL%20GEBIED%20NAAM",
          "STRAATNAAM CORRESPONDENTIEADRES": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#STRAATNAAM%20CORRESPONDENTIEADRES",
          "POSTCODE CORRESPONDENTIEADRES": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#POSTCODE%20CORRESPONDENTIEADRES",
          "GEMEENTENUMMER": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#GEMEENTENUMMER",
          "ONDERWIJSGEBIED NAAM": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#ONDERWIJSGEBIED%20NAAM",
          "PLAATSNAAM": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#PLAATSNAAM",
          "ONDERWIJSSTRUCTUUR": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#ONDERWIJSSTRUCTUUR",
          "PLAATSNAAM CORRESPONDENTIEADRES": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#PLAATSNAAM%20CORRESPONDENTIEADRES",
          "DENOMINATIE": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#DENOMINATIE",
          "COROPGEBIED NAAM": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv#COROPGEBIED%20NAAM"
        },
        "@id": "https://api.duo.nl/v0/datasets/01.-hoofdvestigingen-vo/search?brin=18BR",
        "results": [
          {
            "TELEFOONNUMMER": "0592340973",
            "STRAATNAAM": "Zwartwatersweg",
            "COROPGEBIED CODE": "07",
            "ONDERWIJSGEBIED CODE": "04",
            "HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES": "202",
            "INSTELLINGSNAAM": "School voor Praktijkonderwijs Assen",
            "RPA-GEBIED CODE": "03",
            "HUISNUMMER-TOEVOEGING": "202",
            "RMC-REGIO CODE": "07",
            "WGR-GEBIED NAAM": "Noord- en Midden-Drenthe",
            "PROVINCIE": "Drenthe",
            "INTERNETADRES": "www.pro-assen.nl",
            "BEVOEGD GEZAG NUMMER": "10053",
            "NODAAL GEBIED CODE": "11",
            "POSTCODE CORRESPONDENTIEADRES": "9406 NN",
            "POSTCODE": "9406 NN",
            "WGR-GEBIED CODE": "07",
            "RPA-GEBIED NAAM": "Centraal-Groningen",
            "RMC-REGIO NAAM": "Noord- en midden-Drenthe",
            "GEMEENTENAAM": "ASSEN",
            "NODAAL GEBIED NAAM": "Assen",
            "STRAATNAAM CORRESPONDENTIEADRES": "Zwartwatersweg",
            "ONDERWIJSSTRUCTUUR": "PRO",
            "ONDERWIJSGEBIED NAAM": "Assen-Hoogeveen-Emmen",
            "PLAATSNAAM": "ASSEN",
            "GEMEENTENUMMER": "0106",
            "PLAATSNAAM CORRESPONDENTIEADRES": "ASSEN",
            "DENOMINATIE": "Openbaar",
            "COROPGEBIED NAAM": "Noord-Drenthe",
            "BRIN NUMMER": "18BR"
          }
        ]
      }
