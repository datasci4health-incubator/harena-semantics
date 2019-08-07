import xml.etree.ElementTree as et
import pysolr, json, os

from model.topic import Topic

TOPICS_FILE_LOCATION = '../resources/topics2014.xml'
SOLR_URL = 'http://' + os.environ['SOLR_HOST'] + ':8983/solr/'

PMC_URL = SOLR_URL + 'pmc3/'

treatmentFilter = "article-type:\'randomized controlled trial\' " \
         "title:randomized abstract:randomized " \
         "title:placebo abstract:placebo"


diagnosisFilter = "title:sensitiv* abstract:sensitiv* " \
"kwd:\'sensitivity and specificity\' " \
"+(title:predictive abstract:predictive) +(title:value* abstract:value*) " \
"kwd:'predictive value of tests\' " \
"title:accuracy* abstract:accuracy*"

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
    results = solr.search(diagnosisFilter)
    # print(results)
    # solr.ping()
    for result in results:
        print(result['pmc'] + result['title'])

topics = get_topics()

# print(topics)

for topic in topics:
    searchByCategory(topic.description, topic.number)

#
