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
          "dataset_documentation": "https://api.duo.nl/docs/DatasetDocumentation",
          "dataset_name": "https://api.duo.nl/docs/DatasetName",
          "dataset_query": "https://api.duo.nl/docs/DatasetQuery",
          "dataset_source": "https://api.duo.nl/docs/DatasetSource",
          "dataset_url": "https://api.duo.nl/docs/DatasetUrl",
          "results": "https://api.duo.nl/Results"
        },
        "@id": "https://api.duo.nl/v0/search",
        "results": [
          {
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/po/adressen/adressen_po_1.jsp",
            "dataset_name": "01.-hoofdvestigingen-basisonderwijs",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-basisonderwijs.csv",
            "dataset_url": "https://api.duo.nl/v0/datasets/01.-hoofdvestigingen-basisonderwijs"
          },
          {
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/po/adressen/adressen_po_2.jsp",
            "dataset_name": "02.-hoofdvestigingen-speciaal-(basis)onderwijs",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/02.-hoofdvestigingen-speciaal-(basis)onderwijs.csv",
            "dataset_url": "https://api.duo.nl/v0/datasets/02.-hoofdvestigingen-speciaal-%28basis%29onderwijs"
          },
          {
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/po/adressen/adressen_po_4.jsp",
            "dataset_name": "04.-alle-vestigingen-speciaal-(basis)onderwijs",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/04.-alle-vestigingen-speciaal-(basis)onderwijs.csv",
            "dataset_url": "https://api.duo.nl/v0/datasets/04.-alle-vestigingen-speciaal-%28basis%29onderwijs"
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
          "dataset_documentation": "https://api.duo.nl/docs/DatasetDocumentation",
          "dataset_name": "https://api.duo.nl/docs/DatasetName",
          "dataset_query": "https://api.duo.nl/docs/DatasetQuery",
          "dataset_source": "https://api.duo.nl/docs/DatasetSource",
          "dataset_url": "https://api.duo.nl/docs/DatasetUrl",
          "results": "https://api.duo.nl/Results"
        },
        "@id": "https://api.duo.nl/v0/search?dataset_name=hoofdvestigingen",
        "results": [
          {
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/po/adressen/adressen_po_1.jsp",
            "dataset_name": "01.-hoofdvestigingen-basisonderwijs",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-basisonderwijs.csv",
            "dataset_url": "https://api.duo.nl/v0/datasets/01.-hoofdvestigingen-basisonderwijs"
          },
          {
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/vo/adressen/adressen_vo_1.jsp",
            "dataset_name": "01.-hoofdvestigingen-vo",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv",
            "dataset_url": "https://api.duo.nl/v0/datasets/01.-hoofdvestigingen-vo"
          },
          {
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/po/adressen/adressen_po_2.jsp",
            "dataset_name": "02.-hoofdvestigingen-speciaal-(basis)onderwijs",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/02.-hoofdvestigingen-speciaal-(basis)onderwijs.csv",
            "dataset_url": "https://api.duo.nl/v0/datasets/02.-hoofdvestigingen-speciaal-%28basis%29onderwijs"
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
          "dataset_documentation": "https://api.duo.nl/docs/DatasetDocumentation",
          "dataset_name": "https://api.duo.nl/docs/DatasetName",
          "dataset_query": "https://api.duo.nl/docs/DatasetQuery",
          "dataset_source": "https://api.duo.nl/docs/DatasetSource",
          "dataset_url": "https://api.duo.nl/docs/DatasetUrl",
          "results": "https://api.duo.nl/Results"
        },
        "@id": "https://api.duo.nl/v0/search?field_name=vestigingsnummer",
        "results": [
          {
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/po/adressen/adressen_po_4.jsp",
            "dataset_name": "04.-alle-vestigingen-speciaal-(basis)onderwijs",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/04.-alle-vestigingen-speciaal-(basis)onderwijs.csv",
            "dataset_url": "https://api.duo.nl/v0/datasets/04.-alle-vestigingen-speciaal-%28basis%29onderwijs"
          },
          {
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/po/adressen/adressen_po_3.jsp",
            "dataset_name": "03.-alle-vestigingen-basisonderwijs",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/03.-alle-vestigingen-basisonderwijs.csv",
            "dataset_url": "https://api.duo.nl/v0/datasets/03.-alle-vestigingen-basisonderwijs"
          },
          {
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/po/adressen/adressen_po_9.jsp",
            "dataset_name": "09.-instellingen-per-samenwerkingsverband-passend-onderwijs-po",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/09.-instellingen-per-samenwerkingsverband-passend-onderwijs-po.csv",
            "dataset_url": "https://api.duo.nl/v0/datasets/09.-instellingen-per-samenwerkingsverband-passend-onderwijs-po"
          },
          ...
        ]
      }

Search all datasets on a specific field
---------------------------------------

.. http:get:: /search?(field_name)=(value)

   Use this API call to retrieve all datasets which contain a field with a specific value. Not all fields can be searched. The field names that can be searched are:

   +------------------+--------------------------------------------------------------------------------+
   | *field_name*     | *field_name(s) in datasets*                                                    |
   +------------------+--------------------------------------------------------------------------------+
   | brin             | brin_nummer, brinvestigingsnummer                                              |
   +------------------+--------------------------------------------------------------------------------+
   | bevoegd_gezag    | bevoegd_gezag, bevoegd_gezag_nummer, bevoegd_gezag_school, administratienummer |
   +------------------+--------------------------------------------------------------------------------+
   | instellingsnaam  | instellingsnaam, instellingsnaam_vestiging                                     |
   +------------------+--------------------------------------------------------------------------------+
   | vestigingsnaam   | vestigingsnaam, instellingsnaam_vestiging                                      |
   +------------------+--------------------------------------------------------------------------------+
   | vestigingsnummer | vestigingsnummer, brinvestigingsnummer                                         |
   +------------------+--------------------------------------------------------------------------------+
   | gemeentenaam     | gemeentenaam                                                                   |
   +------------------+--------------------------------------------------------------------------------+
   | gemeentenummer   | gemeentenummer                                                                 |
   +------------------+--------------------------------------------------------------------------------+
   | plaatsnaam       | plaatsnaam, plaatsnaam_vestiging                                               |
   +------------------+--------------------------------------------------------------------------------+
   | postcode         | postcode, postcode_vestiging                                                   |
   +------------------+--------------------------------------------------------------------------------+
   | provincie        | provincie                                                                      |
   +------------------+--------------------------------------------------------------------------------+
   | internet         | internet, internetadres                                                        |
   +------------------+--------------------------------------------------------------------------------+

   As you can see, some of the field names are not standardized accross datasets. For example when you search using the ``bevoegd_gezag`` field name, the actual field names in the datasets can be ``bevoegd_gezag``, ``bevoegd_gezag_nummer``, ``bevoegd_gezag_school`` or ``administratienummer``. This is not a problem when using this API call, because it does search all the different variations of the ``bevoegd_gezag`` field in all datasets. Just be aware that the the field name might be different when you use the resulting datasets.

   In the example below we retrieve all datasets which have a ``brin`` field with the value ``00LY``.

   **Example request**

     https://api.duo.nl/v0/search?brin=00LY

   **Example response** (formatted and limited to 3 results for readability)

    .. sourcecode:: http

      {
        "@context": {
          "dataset_documentation": "https://api.duo.nl/docs/DatasetDocumentation",
          "dataset_name": "https://api.duo.nl/docs/DatasetName",
          "dataset_query": "https://api.duo.nl/docs/DatasetQuery",
          "dataset_source": "https://api.duo.nl/docs/DatasetSource",
          "dataset_url": "https://api.duo.nl/docs/DatasetUrl",
          "results": "https://api.duo.nl/Results"
        },
        "@id": "https://api.duo.nl/v0/search?brin=00LY",
        "results": [
          {
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/vo/adressen/adressen_vo_1.jsp",
            "dataset_name": "01.-hoofdvestigingen-vo",
            "dataset_query": "https://api.duo.nl/v0/datasets/01.-hoofdvestigingen-vo/search?uni_brin=00LY",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv",
            "dataset_url": "https://api.duo.nl/v0/datasets/01.-hoofdvestigingen-vo"
          },
          {
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/vo/Leerlingen/leerlingen_vo_1.jsp",
            "dataset_name": "01.-leerlingen-vo-per-vestiging-naar-onderwijstype-2014-2015",
            "dataset_query": "https://api.duo.nl/v0/datasets/01.-leerlingen-vo-per-vestiging-naar-onderwijstype-2014-2015/search?uni_brin=00LY",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/01.-leerlingen-vo-per-vestiging-naar-onderwijstype-2014-2015.csv",
            "dataset_url": "https://api.duo.nl/v0/datasets/01.-leerlingen-vo-per-vestiging-naar-onderwijstype-2014-2015"
          },
          {
            "dataset_documentation": "https://www.duo.nl/open_onderwijsdata/databestanden/vo/Leerlingen/leerlingen_vo_1.jsp",
            "dataset_name": "01.-leerlingen-vo-per-vestiging-naar-onderwijstype-2013-2014",
            "dataset_query": "https://api.duo.nl/v0/datasets/01.-leerlingen-vo-per-vestiging-naar-onderwijstype-2013-2014/search?uni_brin=00LY",
            "dataset_source": "https://www.duo.nl/open_onderwijsdata/images/01.-leerlingen-vo-per-vestiging-naar-onderwijstype-2013-2014.csv",
            "dataset_url": "https://api.duo.nl/v0/datasets/01.-leerlingen-vo-per-vestiging-naar-onderwijstype-2013-2014"
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
        "@id": "https://api.duo.nl/v0/datasets/06.-bevoegde-gezagen-speciaal-(basis)onderwijs",
        "@context": {
          "STRAATNAAM CORRESPONDENTIEADRES": "https://www.lod.duo.nl/inf/id/begrip/StraatnaamCorrespondentieadres",
          "HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES": "https://www.lod.duo.nl/inf/id/begrip/HuisnummerToevoegingCorrespondentieadres",
          "BEVOEGD GEZAG NAAM": "https://www.lod.duo.nl/inf/id/begrip/BevoegdGezagNaam",
          "TELEFOONNUMMER": "https://www.lod.duo.nl/inf/id/begrip/Telefoonnummer",
          "PLAATSNAAM": "https://www.lod.duo.nl/inf/id/begrip/Plaatsnaam",
          "BEVOEGD GEZAG NUMMER": "https://www.lod.duo.nl/inf/id/begrip/BevoegdGezagNummer",
          "GEMEENTENAAM": "https://www.lod.duo.nl/inf/id/begrip/Gemeentenaam",
          "PLAATSNAAM CORRESPONDENTIEADRES": "https://www.lod.duo.nl/inf/id/begrip/PlaatsnaamCorrespondentieadres",
          "SOORT PRIMAIR ONDERWIJS": "https://www.lod.duo.nl/inf/id/begrip/SoortPrimairOnderwijs",
          "DENOMINATIE": "https://www.lod.duo.nl/inf/id/begrip/Denominatie",
          "results": "https://api.duo.nl/Results",
          "STRAATNAAM": "https://www.lod.duo.nl/inf/id/begrip/Straatnaam",
          "HUISNUMMER-TOEVOEGING": "https://www.lod.duo.nl/inf/id/begrip/HuisnummerToevoeging",
          "POSTCODE": "https://www.lod.duo.nl/inf/id/begrip/Postcode",
          "ADMINISTRATIEKANTOORNUMMER": "https://www.lod.duo.nl/inf/id/begrip/Administratiekantoornummer",
          "INTERNETADRES": "https://www.lod.duo.nl/inf/id/begrip/Internetadres",
          "POSTCODE CORRESPONDENTIEADRES": "https://www.lod.duo.nl/inf/id/begrip/PostcodeCorrespondentieadres",
          "GEMEENTENUMMER": "https://www.lod.duo.nl/inf/id/begrip/Gemeentenummer"
        },
        "results": [
          {
            "STRAATNAAM CORRESPONDENTIEADRES": "Postbus",
            "HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES": "5022",
            "BEVOEGD GEZAG NAAM": "Stichting Mytylschool Tilburg",
            "PLAATSNAAM": "TILBURG",
            "TELEFOONNUMMER": "          ",
            "GEMEENTENAAM": "TILBURG",
            "PLAATSNAAM CORRESPONDENTIEADRES": "TILBURG",
            "SOORT PRIMAIR ONDERWIJS": "(V)SO",
            "DENOMINATIE": "Rooms-Katholiek",
            "STRAATNAAM": "Professor Stoltehof",
            "HUISNUMMER-TOEVOEGING": "1",
            "POSTCODE": "5022 KE",
            "ADMINISTRATIEKANTOORNUMMER": "401",
            "INTERNETADRES": "                                                                                ",
            "POSTCODE CORRESPONDENTIEADRES": "5004 EA",
            "BEVOEGD GEZAG NUMMER": "20233",
            "GEMEENTENUMMER": "0855"
          },
          {
            "STRAATNAAM CORRESPONDENTIEADRES": "Postbus",
            "HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES": "1377",
            "BEVOEGD GEZAG NAAM": "Stichting Vitus Zuid",
            "PLAATSNAAM": "EINDHOVEN",
            "TELEFOONNUMMER": "0402902345",
            "GEMEENTENAAM": "EINDHOVEN",
            "PLAATSNAAM CORRESPONDENTIEADRES": "EINDHOVEN",
            "SOORT PRIMAIR ONDERWIJS": "(V)SO",
            "DENOMINATIE": "Overige",
            "STRAATNAAM": "Toledolaan",
            "HUISNUMMER-TOEVOEGING": "3",
            "POSTCODE": "5629 CC",
            "ADMINISTRATIEKANTOORNUMMER": "413",
            "INTERNETADRES": "www.vituszuid.nl",
            "POSTCODE CORRESPONDENTIEADRES": "5602 BJ",
            "BEVOEGD GEZAG NUMMER": "21657",
            "GEMEENTENUMMER": "0772"
          },
          {
            "STRAATNAAM CORRESPONDENTIEADRES": "Postbus",
            "HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES": "59264",
            "BEVOEGD GEZAG NAAM": "Stichting VierTaal",
            "PLAATSNAAM": "AMSTERDAM",
            "TELEFOONNUMMER": "0206698194",
            "GEMEENTENAAM": "AMSTERDAM",
            "PLAATSNAAM CORRESPONDENTIEADRES": "AMSTERDAM",
            "SOORT PRIMAIR ONDERWIJS": "(V)SO",
            "DENOMINATIE": "Openbaar",
            "STRAATNAAM": "Jan Sluijtersstraat",
            "HUISNUMMER-TOEVOEGING": "3",
            "POSTCODE": "1062 CJ",
            "ADMINISTRATIEKANTOORNUMMER": "780",
            "INTERNETADRES": "www.viertaal.nl",
            "POSTCODE CORRESPONDENTIEADRES": "1040 KG",
            "BEVOEGD GEZAG NUMMER": "21679",
            "GEMEENTENUMMER": "0363"
          },
          ..
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
        "@id": "https://api.duo.nl/v0/datasets/01.-hoofdvestigingen-vo/search?brin=18BR",
        "@context": {
          "STRAATNAAM CORRESPONDENTIEADRES": "https://www.lod.duo.nl/inf/id/begrip/StraatnaamCorrespondentieadres",
          "NODAAL GEBIED NAAM": "https://www.lod.duo.nl/inf/id/begrip/NodaalGebiedNaam",
          "GEMEENTENAAM": "https://www.lod.duo.nl/inf/id/begrip/Gemeentenaam",
          "results": "https://api.duo.nl/Results",
          "RMC-REGIO NAAM": "https://www.lod.duo.nl/inf/id/begrip/RmcRegioNaam",
          "RPA-GEBIED NAAM": "https://www.lod.duo.nl/inf/id/begrip/RpaGebiedNaam",
          "WGR-GEBIED CODE": "https://www.lod.duo.nl/inf/id/begrip/WgrGebiedCode",
          "POSTCODE": "https://www.lod.duo.nl/inf/id/begrip/Postcode",
          "POSTCODE CORRESPONDENTIEADRES": "https://www.lod.duo.nl/inf/id/begrip/PostcodeCorrespondentieadres",
          "GEMEENTENUMMER": "https://www.lod.duo.nl/inf/id/begrip/Gemeentenummer",
          "ONDERWIJSGEBIED NAAM": "https://www.lod.duo.nl/inf/id/begrip/OnderwijsgebiedNaam",
          "PLAATSNAAM": "https://www.lod.duo.nl/inf/id/begrip/Plaatsnaam",
          "ONDERWIJSSTRUCTUUR": "https://www.lod.duo.nl/inf/id/begrip/Onderwijsstructuur",
          "PLAATSNAAM CORRESPONDENTIEADRES": "https://www.lod.duo.nl/inf/id/begrip/PlaatsnaamCorrespondentieadres",
          "DENOMINATIE": "https://www.lod.duo.nl/inf/id/begrip/Denominatie",
          "COROPGEBIED NAAM": "https://www.lod.duo.nl/inf/id/begrip/CoropgebiedNaam",
          "BRIN NUMMER": "https://www.lod.duo.nl/inf/id/begrip/BrinNummer",
          "NODAAL GEBIED CODE": "https://www.lod.duo.nl/inf/id/begrip/NodaalGebiedCode",
          "BEVOEGD GEZAG NUMMER": "https://www.lod.duo.nl/inf/id/begrip/BevoegdGezagNummer",
          "INTERNETADRES": "https://www.lod.duo.nl/inf/id/begrip/Internetadres",
          "PROVINCIE": "https://www.lod.duo.nl/inf/id/begrip/Provincie",
          "WGR-GEBIED NAAM": "https://www.lod.duo.nl/inf/id/begrip/WgrGebiedNaam",
          "RMC-REGIO CODE": "https://www.lod.duo.nl/inf/id/begrip/RmcRegioCode",
          "HUISNUMMER-TOEVOEGING": "https://www.lod.duo.nl/inf/id/begrip/HuisnummerToevoeging",
          "RPA-GEBIED CODE": "https://www.lod.duo.nl/inf/id/begrip/RpaGebiedCode",
          "INSTELLINGSNAAM": "https://www.lod.duo.nl/inf/id/begrip/Instellingsnaam",
          "HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES": "https://www.lod.duo.nl/inf/id/begrip/HuisnummerToevoegingCorrespondentieadres",
          "ONDERWIJSGEBIED CODE": "https://www.lod.duo.nl/inf/id/begrip/OnderwijsgebiedCode",
          "COROPGEBIED CODE": "https://www.lod.duo.nl/inf/id/begrip/CoropgebiedCode",
          "STRAATNAAM": "https://www.lod.duo.nl/inf/id/begrip/Straatnaam",
          "TELEFOONNUMMER": "https://www.lod.duo.nl/inf/id/begrip/Telefoonnummer"
        },
        "results": [
          {
            "STRAATNAAM CORRESPONDENTIEADRES": "Zwartwatersweg",
            "NODAAL GEBIED NAAM": "Assen",
            "GEMEENTENAAM": "ASSEN",
            "RMC-REGIO NAAM": "Noord- en midden-Drenthe",
            "RPA-GEBIED NAAM": "Centraal-Groningen",
            "WGR-GEBIED CODE": "07",
            "POSTCODE": "9406 NN",
            "POSTCODE CORRESPONDENTIEADRES": "9406 NN",
            "ONDERWIJSSTRUCTUUR": "PRO",
            "ONDERWIJSGEBIED NAAM": "Assen-Hoogeveen-Emmen",
            "PLAATSNAAM": "ASSEN",
            "GEMEENTENUMMER": "0106",
            "PLAATSNAAM CORRESPONDENTIEADRES": "ASSEN",
            "DENOMINATIE": "Openbaar",
            "COROPGEBIED NAAM": "Noord-Drenthe",
            "BRIN NUMMER": "18BR",
            "NODAAL GEBIED CODE": "11",
            "BEVOEGD GEZAG NUMMER": "10053",
            "INTERNETADRES": "www.pro-assen.nl",
            "PROVINCIE": "Drenthe",
            "WGR-GEBIED NAAM": "Noord- en Midden-Drenthe",
            "RMC-REGIO CODE": "07",
            "HUISNUMMER-TOEVOEGING": "202",
            "RPA-GEBIED CODE": "03",
            "INSTELLINGSNAAM": "School voor Praktijkonderwijs Assen",
            "HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES": "202",
            "ONDERWIJSGEBIED CODE": "04",
            "COROPGEBIED CODE": "07",
            "STRAATNAAM": "Zwartwatersweg",
            "TELEFOONNUMMER": "0592340973"
          }
        ]
      }
