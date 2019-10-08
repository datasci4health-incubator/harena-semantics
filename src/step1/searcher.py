import xml.etree.ElementTree as et
import pysolr, json, os
from ncbo.ncbo_annotator import get_mesh_terms

from model.topic import Topic

SOLR_URL = 'http://' + os.environ['SOLR_HOST'] + ':8983/solr/pmc'
TOPICS_FILE_LOCATION = './step1/resources/topics2014.xml'

if not os.path.exists('./results'):
    os.makedirs('./results')


def get_topics():
    tree = et.parse(TOPICS_FILE_LOCATION)
    print(tree)
    topics_et = tree.getroot()
    topics = []

    for topic_et in topics_et:
        type = topic_et.attrib['type']
        number = topic_et.attrib['number']
        description = topic_et.find("description").text
        description = description.replace(':', '\:')

        summary = topic_et.find("summary").text

        topic = Topic(description, summary, number, type)

        topics.append(topic)
    return topics


def get_query_from_mesh_terms(mesh_terms):
    query_search = ''

    for mesh_term in mesh_terms:
        aux = mesh_term.split()
        compound_term = ''
        if len(aux) > 1:
            compound_term = '('

            for x in aux:
                compound_term = compound_term + '+' + x + ' '
            compound_term = compound_term + ')'
            query_search = query_search + compound_term + ' '
        else:
            query_search = query_search + mesh_term + ' '
    return query_search


def search_by_category(field, query_search, filter):
    solr = pysolr.Solr(SOLR_URL)
    query = field + ':' + query_search
    retrieved_docs = solr.search(q=query, fq=filter)
    pmcs = []
    for doc in retrieved_docs:
        pmcs.append(doc['pmc'])
    return pmcs


with open('./step1/resources/filters.json') as f:
    filters = json.load(f)

mesh_results = []
description_results = []
topics = get_topics()

for topic in topics:
    for filter in filters:
        filter1 = filters.get(filter)
        print(filter1)
        pmcs = search_by_category(topic.description, filter1)
        result = {'topic':topic.number, 'pmc':pmcs, 'clinical property': filter}
        results.append(result)
