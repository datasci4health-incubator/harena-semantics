import os, json
import pysolr
import xml.etree.ElementTree as et

URL = 'http://' + os.environ['SOLR_HOST'] + ':8983/solr/pmc'

solr = pysolr.Solr(URL, results_cls=dict)

solr.add([
    {
        "id": "doc_1",
        "title": "A test document invocado",
    },
    {
        "id": "doc_2",
        "title": "The avocado: Tasty or Dangerous?",
        "_doc": [
            {"id": "child_doc_1", "title": "peel"},
            {"id": "child_doc_2", "title": "seed"},
        ]
    },
])
with os.scandir('../../documents/pmc') as entries1:
    # Two chained for loops iterate over the original folder structure of the CDS Track
    for entry1 in entries1:
        print(entry1.name)
        with os.scandir(entry1.path) as entries2:
            for entry2 in entries2:
                print(entry2.name)
                with os.scandir(entry2.path) as documents:
                    i = 0

                    # Here we have each document in fact
                    for document in documents:
                        i = i + 1
                        print(document.path)
                        tree = et.parse(document.path)
                        article_et = tree.getroot()

                        article = dict()
                        article.update({'article-type': article_et.attrib.get('article-type')})

                        articles_id = []
                        for article_id_et in article_et.findall("./front/article-meta/article-id"):
                            article_id = dict()
                            article_id.update({'pub-id-type': article_id_et.attrib.get('pub-id-type')})
                            article_id.update({'value': article_id_et.text})
                            articles_id.append(article_id)
                            article.update({'article-id': articles_id})

                        title_group_et = article_et.find("./front/article-meta/title-group")

                        if title_group_et is not None:
                            title_group = dict()

                            if title_group_et.find('article-title') is not None:
                                title_group.update({'article-title': title_group_et.find('article-title').text})

                            article.update({'title-group': title_group})

                            subtitles = []
                            for subtitle_et in title_group_et.findall('subtitle'):
                                subtitles.append(subtitle_et.text)
                                title_group.update({'subtitle': subtitles})

                        abstracts = []
                        for abstract_et in article_et.findall("./front/article-meta/abstract"):
                            abstract = dict()

                            ps = []
                            for p in abstract_et.findall('p'):
                                ps.append(p.text)
                                abstract.update({'p': ps})

                            secs = []
                            for sec_et in abstract_et.findall('sec'):
                                sec = dict()

                                if sec_et.find('title') is not None:
                                    sec.update({'title': sec_et.find('title').text})

                                if sec_et.find('p') is not None:
                                    sec.update({'p': sec_et.find('p').text})
                                secs.append(sec)
                                abstract.update({'sec': secs})

                            abstracts.append(abstract)
                            article.update({'abstract': abstracts})

                        kwd_groups = []
                        for kwd_group_et in article_et.findall("./front/article-meta/kwd-group"):
                            kwd_group = dict()

                            kwds = []
                            for kwd_et in kwd_group_et.findall("kwd"):
                                print(kwd_et.text)
                                kwds.append(kwd_et.text)

                            kwd_group.update({'kwd': kwds})
                            kwd_groups.append(kwd_group)
                            article_id.update({'kwd-groups': kwd_groups})

                        bodies = []
                        for body_et in article_et.findall('./body'):
                            body = dict()

                            ps = []
                            for p in body_et.findall('p'):
                                ps.append(p.text)
                                body.update({'p': ps})

                            secs = []
                            for sec_et in body_et.findall('sec'):
                                sec = dict()

                                if sec_et.find('title') is not None:
                                    sec.update({'title': sec_et.find('title').text})

                                if sec_et.find('p') is not None:
                                    sec.update({'p': sec_et.find('p').text})
                                secs.append(sec)
                                body.update({'sec': secs})
                            bodies.append(body)
                            article.update({'body': bodies})

                        print(article)
                        with open('data.json', 'w') as fp:
                            json.dump(article, fp)

                        solr = pysolr.Solr(URL, results_cls=dict)

                        solr.add([article])
                    print('Documents processed:')
print(i)

solr.commit()
