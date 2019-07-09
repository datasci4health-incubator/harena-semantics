import os
import pysolr
import xml.etree.ElementTree as et

URL = 'http://' + os.environ['SOLR_HOST'] + ':8983/solr/pmc'

solr = pysolr.Solr(URL, results_cls=dict)

with os.scandir('../../documents/pmc') as entries1:
    for entry1 in entries1:
        print(entry1.path)
        with os.scandir(entry1.path) as entries2:
            for entry2 in entries2:
                print(entry2.name)
                with os.scandir(entry2.path) as documents:
                    i = 0
                    for document in documents:
                        i = i+1
                        print(document.name)
                        tree = et.parse(document.path)
                        root = tree.getroot()
                        print(root.tag)

                        first = dict()
                        for title in root.findall("./front/article-meta/title-group/article-title"):
                            print('title')
                            first.update({'title': title.text})

                        for abstract in root.findall("./front/article-meta/abstract/p"):
                            first.update({'abstract': abstract.text})

                        solr = pysolr.Solr(URL, results_cls=dict)
                        print(first)

                        solr.add([
                            {
                                "title": first.get('title'),
                                "abstract": first.get('abstract')
                            }
                        ])
                    print('Documents processed:')
print(i)