import os, json, pysolr
import xml.etree.ElementTree as et

from src.experiments.model.topic import Topic
from src.step1.searcher import Searcher

SOLR_URL = 'http://' + os.environ['SOLR_HOST'] + ':8983/solr/pmc'

TOPICS_FILE_LOCATION = "src/experiments/resources/topics2014.xml"
FILTERS_LOCATION = "src/experiments/resources/filters.json"

def get_filters():
    with open(FILTERS_LOCATION) as f:
        return json.load(f)

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

def write_topic_result(filter, results):
    if not os.path.exists('src/experiments/first/results/'):
        os.makedirs('src/experiments/first/results/')

    with open('src/experiments/first/results/' + filter + '.json', 'w') as outfile:
        json.dump(results, outfile)

def perform():
    filters = get_filters()
    topics = get_topics()

    for filter in filters:
        results = []

        query_filter = filters.get(filter)
        print(query_filter)

        for topic in topics:
            print(topic.description)

            s = Searcher()
            related_papers = s.search_by_category('chest pain',
                                                  'type:\'randomized controlled trial\' title:randomized abstract:randomized title:placebo abstract:placebo')

            titles = []
            for paper in related_papers:
                if paper.get('title') is not None:
                    titles.append(paper.get('title'))

            result = {'Description':topic.description, 'Papers':titles}
            results.append(result)

            write_topic_result(filter, results)

            return results