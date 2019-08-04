import xml.etree.ElementTree as et
import json
from model.topic import Topic

TOPICS_FILE_LOCATION = '../resources/topics2014.xml'

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

print(topics)
