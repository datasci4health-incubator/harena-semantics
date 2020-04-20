# Harena ASM - Authoring Support Module
## A [Harena](https://github.com/datasci4health/harena)'s module to support Clinical Cases authoring task

## Table of Contents 

* [Table of Contents](#table-of-contents)
* [Overview](#overview)
* [Getting Started](#getting-started)
  * [Running as Docker containers](#running-as-docker-containers)
* [Performing Searches](#peforming-searches)

<!-- * [System Requirements](#system-requirements)
  * [For running as Docker containers](#for-running-as-linuxwindows-docker-containers)
  * [For running locally](#for-running-locally)
* [Configuration](#configuration)
  * [Virtualenvs: AdonisJS](#virtualenvs-adonisjs)
  * [Virtualenvs: Database](#virtualenvs-database)
* [Contributing](#contributing)
  * [Project organization](#project-organization)
  * [Branch organization (future CI/CD)](#branch-organization-future-cicd)-->

## Overview

ASM indexes a papers collection to enable efficient search over it.

Papers collection is from http://www.trec-cds.org/2014.html. 

The collection is automatically downloaded through the installation process (`docker-compose` command)

## Getting Started

### Running as Docker containers

At the ```harena-asm``` root folder run the command to start the docker container:

```docker-compose -f docker-compose-dev.yml up```

As the start process is done, you must access the following endpoint in order to index the papers:  

```buildoutcfg
GET http://localhost:5000/indexer
```

 you can get access to the container through the sh:

```bash
docker exec -it harena-asm sh
```

You can access ASM at http://localhost:5000
You can access SOLR admin at http://localhost:8983

## Performing Searches

```buildoutcfg
POST http://localhost:5000/searcher

params: description (text)
```