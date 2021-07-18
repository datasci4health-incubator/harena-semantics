# Harena Semantics

A module to manage Semantic Clinical Cases. 
Visit [Harena: https://github.com/harena-lab](https://github.com/harena-lab).

<!-- ## Available Services

Check https://documenter.getpostman.com/view/12184223/TzK2ZE4d to discover available endpoints provided by `harena manager api`.
 -->
## Getting Started

We provide a `docker container` to locally run `harena-semantics` code. Containers guarantee the required minimal configuration to run the code. Read [docker](https://docs.docker.com/install/) e [docker-compose](https://docs.docker.com/compose/install/) documentations to install docker and learn further about containers.

> In order to execute `docker` without `sudo`, read this link: https://docs.docker.com/engine/install/linux-postinstall/, which shows another optional and valuable configurations in docker environment.

#### Instructions (for Linux users)

Clone `harena-semantics` repository, get into it, checkout `master` branch, and build the Semantics docker image:

```bash
git clone https://github.com/datasci4health-incubator/harena-semantics.git
cd harena-semantics
git pull origin master

docker build . -t semantics
```

Start up the docker container:

```bash
docker-compose -f docker-compose-dev.yml up
```

Once the start up process is done, access http://localhost:10040/ to check if the system is properly working.

If you want to get the command line of the container, then run the command:

```bash
docker exec -it harena-semantics bash
```
## Available Services

- `POST /ner/bert`: Annotates the input text with named entities recognized through a BERT-based neural network.
- `POST /ner/ncbo`: Annotates the input text with ontology concepts recognized via the NCBO Annotator service.  

<!-- You can access Indexer at http://localhost:5000
You can access SOLR admin at http://localhost:8983 -->

<!-- ## Performing Searches -->
<!-- 
```buildoutcfg
POST http://localhost:5000/searcher

params: description (text)
```
 -->
