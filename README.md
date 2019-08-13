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

At the ```harena-asm/``` root folder run the command to start the docker container:

```docker-compose up```

Solr admin: http://localhost:8983/solr

To index PMC papers: 

```
cd src/
pipenv run python src/step1/indexer.py
```
