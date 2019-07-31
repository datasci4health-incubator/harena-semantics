import xml.etree.ElementTree as et

TOPICS_FILE_LOCATION = '../resources/topics2014.xml'

tree = et.parse(TOPICS_FILE_LOCATION)

topics_et = tree.getroot()
topics = []

for topic_et in topics_et:
    topic = dict()

    topic.update(topic_et.attrib)

    description = topic_et.find("description").text
    summary = topic_et.find("summary").text

    topic.update({ 'description': description })
    topic.update({ 'summary': summary })

    print(topic)
    topics.append(topic)

print(topics)
