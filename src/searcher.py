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

prognosisFilter = "kwd:prognosis " \
                  "title:diagnosed abstract:diagnosed " \
                  "title:cohort* abstract:cohort* " \
                  "kwd:'cohort effect' " \
                  "kwd:'cohort studies' " \
                  "title:predictor* abstract:predictor* " \
                  "title:death abstract:death " \
                  "kwd:'models, statistical'"
etiologyFilter = "title:risk abstract:risk " \
                 "kwd:risk " \
                 "title:mortality abstract:mortality " \
                 "kwd:mortality " \
                 "title:cohort abstract:cohort"
reviewFilter = "article-type:'meta analysis' article-type:review " \
               "title:'meta analysis' abstract:'meta analysis' " \
               "kwd:'meta analysis' " \
               "title:search* abstract:search*"

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
        break
    return topics

# def filterPapers():

def search_by_category(topic_description, filter):
    solr = pysolr.Solr(PMC_URL)
    filter_queries = ['title:meta analysis']
    print(topic_description)
    results = solr.search('body:'+topic_description, fq=filter)
    # print(results)
    # solr.ping()
    for result in results:
        print(result['title'])

topics = get_topics()

for topic in topics:
    search_by_category(topic.description, diagnosisFilter)
