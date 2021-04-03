# Harena ASM - Annotation Support Module

A [Harena](https://github.com/harena-lab)'s module to support Clinical Cases annotation
ASM Content Annotation. Suggestion system. 

## Available Services

Currently, ASM provides REST endpoints grouped into 2 categories:
- Biomedical Named Entity Recognition endpoints, which Recognize biomedical concepts in a given text using to different approaches. The return is text annotated in a Verum format
  - `/ner/bern`
  - `/ner/bert`
  - `/ner/ncbo`
  - `/ner/unsupervised` 
- Retrieval of Biomedical scientific articles
  - `/indexer`: indexes papers collection to enable efficient search over it
  - `/indexer/search`: search papers according to needs specified as parameters


Check https://www.getpostman.com/collections/c164e51189e95c3270a5 to discover available endpoints provided by `harena manager api`.

<!-- Papers collection is from http://www.trec-cds.org/2014.html. 

The collection is automatically downloaded through the installation process (`docker-compose` command) -->

## Getting Started

We provide a `docker container` to locally run `harena-asm` code. Containers guarantee the required minimal configuration to run the code. Read [docker](https://docs.docker.com/install/) e [docker-compose](https://docs.docker.com/compose/install/) documentations to install docker and learn further about containers.

> In order to execute `docker` without `sudo`, read this link: https://docs.docker.com/engine/install/linux-postinstall/, which shows another optional and valuable configurations in docker environment.

#### Instructions (for Linux users)

Clone `harena-asm` repository, get into it, checkout `development` branch, and build the manager docker image:

```bash
git clone https://github.com/datasci4health-incubator/harena-asm.git
cd harena-asm
git checkout -b development
git pull origin development

docker build . -t asm
cd ..
```

Start up the docker container:

```bash
docker-compose -f docker-compose-dev.yml up
```

Once the start up process is done, access http://localhost:10040/ to check if the system is working. You can access SOLR admin at http://localhost:8983


If you want to get the command line of the container, then run the command:

```bash
docker exec -it harena-manager_harena-manager_1 bash
```

<!-- As the start process is done, you must access the following endpoint in order to index the papers:  

```buildoutcfg
GET http://localhost:5000/indexer -->
```

 you can get access to the container through the sh:

```bash
docker exec -it harena-asm sh
```
