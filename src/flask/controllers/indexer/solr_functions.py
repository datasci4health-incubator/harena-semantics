import pysolr, json, os
import xml.etree.ElementTree as et
from .entrez_utilities import get_pubtype_and_mesh
from ..ner.ncbo.ncbo_annotator import Annotator

SOLR_URL = 'http://' + os.environ['SOLR_HOST'] + ':8983/solr/pmc'



def search_by_category(description, filter, mode):
    if mode == 'textword':
        search_query = description
    else:
        a = Annotator()


        mesh_terms = a.get_mesh_terms(description)
        search_query = get_query_from_mesh_terms(mesh_terms)
        print('aquiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii ',SOLR_URL)

    solr = pysolr.Solr(SOLR_URL)
    query = 'abstract:' + search_query
    return solr.search(q=query, fq=filter)


def indexer():
    i = 0
    errors = []

    # Three chained for loops iterate over the original folder structure of the CDS Track

    with os.scandir('documents/pmc') as entries1:
        # Here is pmc-text-xx/
        for entry1 in entries1:
            print(entry1.name)

            with os.scandir(entry1.path) as entries2:

                # Here is pmc-text-xx/xx/
                for entry2 in entries2:
                    try:
                        print(entry2.name)
                        articles = []
                        pmids = []

                        with os.scandir(entry2.path) as documents:

                            # Here we have each document in fact
                            for document in documents:
                                try:
                                    print(document.path)
                                    tree = et.parse(document.path)
                                    article_et = tree.getroot()

                                    article = dict()
                                    publication_types = [article_et.attrib.get('article-type')]

                                    for article_id_et in article_et.findall("./front/article-meta/article-id"):
                                        if article_id_et.attrib.get('pub-id-type') == 'pmc':
                                            article.update({'pmc': article_id_et.text})
                                        if article_id_et.attrib.get('pub-id-type') == 'pmid':
                                            article.update({'pmid': article_id_et.text})
                                            pmids.append(article_id_et.text)

                                    title_group_et = article_et.find("./front/article-meta/title-group")

                                    if title_group_et is not None:
                                        if title_group_et.find('article-title') is not None:
                                            article_title_et = title_group_et.find('article-title')
                                            article_title = getValue(article_title_et)
                                            article.update({'title': article_title})
                                            # print(article_title)

                                    abstracts = []
                                    for abstract_et in article_et.findall("./front/article-meta/abstract"):
                                        for p_et in abstract_et.findall('./p'):
                                            abstracts.append(getValue(p_et))

                                        for sec_et in abstract_et.findall('./sec'):
                                            if sec_et.find('title') is not None and sec_et.find('p') is not None:
                                                sec_title_et = sec_et.find('title')
                                                sec_title = getValue(sec_title_et)

                                                p_et = sec_et.find('p')
                                                p = getValue(p_et)

                                                sec = ''
                                                if sec_title is not None:
                                                    sec = sec_title + ': '
                                                if p is not None:
                                                    sec = sec + p
                                                abstracts.append(sec)

                                        article.update({'abstract': abstracts})

                                    bodies = []
                                    for body_et in article_et.findall('./body'):
                                        for p_et in body_et.findall('p'):
                                            p = getValue(p_et)
                                            bodies.append(p)

                                        for sec_et in body_et.findall('sec'):
                                            if sec_et.find('title') is not None:
                                                sec_title_et = sec_et.find('title')
                                                sec_title = getValue(sec_title_et)

                                            if sec_et.find('p') is not None:
                                                p_et = sec_et.find('p')
                                                p = getValue(p_et)

                                            sec = ''
                                            if sec_title is not None:
                                                sec = sec_title + ': '
                                            if p is not None:
                                                sec = sec + p
                                            bodies.append(sec)
                                        article.update({'body': bodies})

                                    articles.append(article)
                                    i = i + 1

                                except et.ParseError:
                                    print('error')

                            result = get_pubtype_and_mesh(pmids)

                            for c in result:
                                filtered_article = filter(lambda article: article.get('pmid') == c.get('pmid'),
                                                          articles)
                                for article in filtered_article:
                                    article.update({'mesh': c.get('mesh_terms')})
                                    article.update({'type': c.get('types')})

                        solr = pysolr.Solr(SOLR_URL, results_cls=dict)

                        solr.add(articles)
                        solr.commit()
                    except:
                        errors.append(entry1.name + entry2.name)
    print('Documents processed:')
    print(i)
    print('Errors:')
    print(errors)


def get_query_from_mesh_terms(mesh_terms):
    query_search = ''

    for mesh_term in mesh_terms:
        aux = mesh_term.split()
        compound_term = ''
        if len(aux) > 1:
            compound_term = '('

            for x in aux:
                compound_term = compound_term + '+' + x + ' '
            compound_term = compound_term + ')'
            query_search = query_search + compound_term + ' '
        else:
            query_search = query_search + mesh_term + ' '
    return query_search


def getValue(element):
    if element.text is not None:
        return "".join(element.text + "".join([et.tostring(e, encoding='unicode') for e in list(element)]))
