import xml.etree.ElementTree as et
import json
from model.topic import Topic

TOPICS_FILE_LOCATION = '../resources/topics2014.xml'

filter = 'randomized controlled trial[Publication Type] OR randomized[Title/Abstract] OR placebo[Title/Abstract]'

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

        # print(topic)
        topic = json.dumps(topic.__dict__)
        topics.append(topic)
    return topics

def filterPapers():


def searchByCategory(topicDescription, topicNumber):


def experiment(topics):
    for topic in topics:
        searchByCategory(topic.description, topic.number)




topics = get_topics()
#
# print(topics)
