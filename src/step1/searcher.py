import xml.etree.ElementTree as et
import pysolr, json, os

from model.topic import Topic

TOPICS_FILE_LOCATION = 'resources/topics2014.xml'

if not os.path.exists('results'):
    os.makedirs('results')

SOLR_URL = 'http://' + os.environ['SOLR_HOST'] + ':8983/solr/pmc3'


def get_topics():
    tree = et.parse(TOPICS_FILE_LOCATION)

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


def search_by_category(topic_description, filter):
    solr = pysolr.Solr(SOLR_URL)

    retrievedDocs = solr.search(filter)
    pmcs = []
    for doc in retrievedDocs:
        pmcs.append(doc['pmc'])
    return pmcs


with open('./resources/filters.json') as f:
    filters = json.load(f)

results = []
topics = get_topics()

for topic in topics:
    filter = filters.get(topic.type)
    if filter is not None:
        pmcs = search_by_category(topic.description, filter)
        result = {'topic':topic.number, 'pmc':pmcs}
        results.append(result)

with open('results/step1-no-description.json', 'w') as outfile:
    json.dump(results, outfile)
