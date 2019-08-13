import os, json
import pysolr
import xml.etree.ElementTree as et

URL = 'http://' + os.environ['SOLR_HOST'] + ':8983/solr/pmc3'

solr = pysolr.Solr(URL, results_cls=dict)


def getValue(element):
    if element.text is not None:
        return "".join(element.text + "".join([et.tostring(e, encoding='unicode') for e in list(element)]))


i = 0
with os.scandir('../documents/pmc') as entries1:
    # Two chained for loops iterate over the original folder structure of the CDS Track
    # Here is pmc-text-xx/
    for entry1 in entries1:
        print(entry1.name)

        # Here is pmc-text-xx/xx/
        with os.scandir(entry1.path) as entries2:
            for entry2 in entries2:
                print(entry2.name)
                articles = []
                with os.scandir(entry2.path) as documents:

                    # Here we have each document in fact
                    for document in documents:
                        try:
                            print(document.path)
                            tree = et.parse(document.path)
                            article_et = tree.getroot()

                            article = dict()
                            article.update({'article-type': article_et.attrib.get('article-type')})

                            for article_id_et in article_et.findall("./front/article-meta/article-id"):
                                if article_id_et.attrib.get('pub-id-type') == 'pmc':
                                    article.update({'pmc': article_id_et.text})

                            title_group_et = article_et.find("./front/article-meta/title-group")

                            if title_group_et is not None:
                                if title_group_et.find('article-title') is not None:
                                    article_title_et = title_group_et.find('article-title')
                                    article_title = getValue(article_title_et)
                                    article.update({'title': article_title})

                                subtitles = []
                                for subtitle_et in title_group_et.findall('subtitle'):
                                    subtitles.append(getValue(subtitle_et))
                                    article.update({'subtitle': subtitles})

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

                            kwds = []
                            for kwd_group_et in article_et.findall("./front/article-meta/kwd-group"):
                                for kwd_et in kwd_group_et.findall("kwd"):
                                    kwds.append(kwd_et.text)

                                article.update({'kwd': kwds})

                            articles.append(article)
                            i = i + 1

                        except et.ParseError:
                            print('error')

                solr = pysolr.Solr(URL, results_cls=dict)

                solr.add(articles)
                solr.commit()

print('Documents processed:')
print(i)
