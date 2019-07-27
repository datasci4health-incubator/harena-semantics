# Harena ASM - Authoring Support Module
## A [Harena](https://github.com/datasci4health/harena)'s module to support Clinical Cases authoring task

## Table of Contents 

* [Table of Contents](#table-of-contents)
* [Getting Started](#getting-started)
  * [Running as Docker containers](#running-as-docker-containers)
<!-- * [System Requirements](#system-requirements)
  * [For running as Docker containers](#for-running-as-linuxwindows-docker-containers)
  * [For running locally](#for-running-locally)
* [Configuration](#configuration)
  * [Virtualenvs: AdonisJS](#virtualenvs-adonisjs)
  * [Virtualenvs: Database](#virtualenvs-database)
* [Contributing](#contributing)
  * [Project organization](#project-organization)
  * [Branch organization (future CI/CD)](#branch-organization-future-cicd)-->

   

## Getting Started

### Running as Docker containers

At the ```harena-asm``` root folder run the command to start the docker container:

```docker-compose -f docker-compose.yml -f docker-compose-dev.yml up```

When start process is done, you can get access to the container through the sh:

```bash
docker exec -it harena-asm sh
```

Inside the harena-asm container, run the following commands in order to index the pmc documents on the solr server:

```bash
cd src/
pipenv run python pmc_indexer.py
```

You can access the solr admin at (http://localhost:8983)



