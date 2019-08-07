import xml.etree.ElementTree as et
import pysolr, json, os

from model.topic import Topic

TOPICS_FILE_LOCATION = '../resources/topics2014.xml'
SOLR_URL = 'http://' + os.environ['SOLR_HOST'] + ':8983/solr/'

PMC_URL = SOLR_URL + 'pmc/'

filter = '\'randomized controlled trial\'[Publication Type]OR ' \
         'title:randomized OR abstract:randomized OR ' \
         'title:placebo OR abstract:placebo'

print(filter)

def get_topics():
    tree = et.parse(TOPICS_FILE_LOCATION)

    topics_et = tree.getroot()
    topics = []

    for topic_et in topics_et:
        type = topic_et.attrib['type']
        number = topic_et.attrib['number']
        description = topic_et.find("description").text
        summary = topic_et.find("summary").text

        topic = Topic(description, summary, number, type)

        # topic1 = json.dumps(topic.__dict__)
        # print(topic1.description)

        topics.append(topic)
    return topics

# def filterPapers():


def searchByCategory(topicDescription, topicNumber):
    solr = pysolr.Solr(PMC_URL)
    results = solr.search('abstract:smoking')
    # print(results)
    # solr.ping()
    for result in results:
        print(result['title'])

topics = get_topics()

# print(topics)

for topic in topics:
    searchByCategory(topic.description, topic.number)

#
