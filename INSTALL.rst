DUO API install notes
#####################

.. contents::

Installation instructions
=============

Install either using Docker, Vagrant or manually.

Install using Docker
------------

Using `Docker <http://www.docker.com/>`_ is by far the easiest way to spin up a development environment and get started with contributing to the DUO API. The following has been tested to work with Docker 1.0.1 and up.

1. Clone the DUO API git repository::

   $ git clone git@github.com:openstate/kamervragen.git
   $ cd kamervragen/

2. Build an image using the Dockerfile, i.e. use Ubuntu as base and install all dependencies, and call it open-state/kamervragen::

   $ docker build -t open-state/kamervragen .

3. Create a container based on the newly created open-state/kamervragen image. The current folder on the host machine (which should be the root of the kamervragen repo!) is mounted on /opt/duo in the container (so you can just develop on your host machine using your favorite development setup). Furthermore port 9200 is mapped from the container to the host machine so you can reach elasticsearch on http://127.0.0.1:9200, the same holds for port 5000 which gives access to the API::

   $ docker run -it --name c-kamervragen -v `pwd`:/opt/duo -p 9200:9200 -p 5000:5000 open-state/kamervragen

4. Once connected to the container the following commands currently still have to be executed manually::

   $ ./start.sh

5. Thereafter you can start extract processes, Ie.:

   $ ./manage.py extract start <source_name>

Elasticsearch is now accessible locally in the Docker container via http://127.0.0.1:9200, or from the host via http://<CONTAINER IP ADDRESS>:9200 (look up the container's IP address using ``docker inspect`` as shown below).

Some useful Docker commands::

   # Show all docker images on your machine
   $ docker images

   # List all containers which are currently running
   $ docker ps

   # List all containers
   $ docker ps -a

   # Connect another shell to a currently running container (useful during development)
   $ docker exec -it <CONTAINER ID/NAME> bash

   # Start a stopped container and automatically attach to it (-a)
   $ docker start -a <CONTAINER ID/NAME>

   # Attach to a running container (use `exec` though if you want to open any extra shells beyond this one)
   $ docker attach <CONTAINER ID/NAME>

   # Return low-level information on a container or image (e.g., a container's IP address)
   $ docker inspect <CONTAINER/IMAGE ID/NAME>

   Also, if attached to a container, either via run, start -a or attach, you can detach by typing CTRL+p CTRL+q


Usage
============

Some quick notes on how to use the DUO API

Running an DUO API extractor
------------

1. Make the necessary changes to the 'sources' settings file (``ocd_backend/sources.json``). For example, fill out any API keys you might need for specific APIs.

2. Start worker processes::

   $ celery --app=ocd_backend:celery_app worker --loglevel=info --concurrency=2

3. In another terminal (in case of Docker, use ``docker exec`` as described above), start the extraction process::

   $ ./manage.py extract start duo

   You can get an overview of the available sources by running ``./manage.py extract list_sources``.

Running the API frontend
------------

Once started, the API can be accessed on port 5000 (again either locally or from the host, similar to accessing elasticsearch as described above)::

   $ ./manage.py frontend runserver

Automatic updating using cron
------------

The ``bin/update.sh`` script contains the instructions to update indices. In the case of docker it is the easiest to add this script to the crontab on the host machine. Using ``sudo crontab -e``, add the following line::

   $ 0 1,7,13,19 * * * sudo docker exec docker_c-kamervragen_1 /opt/duo/bin/update.sh
