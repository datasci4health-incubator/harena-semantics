import os, json, pysolr
import xml.etree.ElementTree as et

from model.topic import Topic
# from first.searcher import search_by_category

TOPICS_FILE_LOCATION = './experiments/resources/topics2014.xml'
SOLR_URL = 'http://' + os.environ['SOLR_HOST'] + ':8983/solr/pmc'

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

def search_by_category(topic_description, filter):
    solr = pysolr.Solr(SOLR_URL)
    query = 'abstract:' + topic_description + 'or body:' + topic_description
    return solr.search(q=query, fq=filter)


with open('./experiments/resources/filters.json') as f:
    filters = json.load(f)

topics = get_topics()

for filter in filters:
    results = []

    query_filter = filters.get(filter)
    print(query_filter)

    for topic in topics:
        print(topic.description)
        related_papers = search_by_category(topic.description, query_filter)

        titles = []
        for paper in related_papers:
            if paper.get('title') is not None:
                titles.append(paper.get('title'))

        result = {'Description':topic.description, 'Paper':titles}
        results.append(result)

        if not os.path.exists('./experiments/first/results/'):
            os.makedirs('./experiments/first/results/')

        with open('./experiments/first/results/' + filter + '.json', 'w') as outfile:
            json.dump(results, outfile)