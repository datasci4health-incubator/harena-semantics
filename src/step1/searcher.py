import xml.etree.ElementTree as et
import pysolr, json, os

from model.topic import Topic

TOPICS_FILE_LOCATION = './step1/resources/topics2014.xml'

if not os.path.exists('./step1/results'):
    os.makedirs('./step1/results')

SOLR_URL = 'http://' + os.environ['SOLR_HOST'] + ':8983/solr/pmc'

def get_topics():
    tree = et.parse(TOPICS_FILE_LOCATION)
    print(tree)
    topics_et = tree.getroot()
    topics = []

    for topic_et in topics_et:
        type = topic_et.attrib
        ['type']
        number = topic_et.attrib['number']
        description = topic_et.find("description").text
        description = description.replace(':', '\:')

        summary = topic_et.find("summary").text

        topic = Topic(description, summary, number, type)

        topics.append(topic)
    return topics


def search_by_category(topic_description, filter):
    solr = pysolr.Solr(SOLR_URL)
    query = 'abstract:' + topic_description + 'or body:' + topic_description
    retrievedDocs = solr.search(q=query, fq=filter)
    pmcs = []
    for doc in retrievedDocs:
        pmcs.append(doc['pmc'])
    return pmcs


with open('./step1/resources/filters.json') as f:
    filters = json.load(f)

results = []
topics = get_topics()

for topic in topics:
    for filter in filters:
        filter1 = filters.get(filter)
        print(filter1)
        pmcs = search_by_category(topic.description, filter1)
        result = {'topic':topic.number, 'pmc':pmcs, 'clinical property': filter}
        results.append(result)


with open('./step1/results/experiment.json', 'w') as outfile:
    json.dump(results, outfile)
