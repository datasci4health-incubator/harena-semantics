import os, sys
import xml.etree.ElementTree as et

# file = os.open('../../documents/pmc/pmc-text-01/09/2771650.nxml', os.O_RDONLY)
# print(file)


def getValue(element):
    print('1')
    print(element.text)
    print('/1')
    # [print(et.tostring(e, encoding='unicode')) for e in list(element)]
    for e in list(element):
        print(2)
        print(e.text)
        print(et.tostring(e, encoding='unicode'))
        print(3)
    return "".join(element.text + "".join([et.tostring(e, encoding='unicode') for e in list(element)]))
    # print(p)
    # return text

try:
    tree = et.parse('../../documents/pmc/pmc-text-01/25/2887896.nxml')

    article_et = tree.getroot()

    title_group_et = article_et.find("./front/article-meta/title-group")

    if title_group_et is not None:
        title_group = dict()

        for abstract_et in article_et.findall("./front/article-meta/abstract"):
            abstract = dict()

            secs = []
            for sec_et in abstract_et.findall('sec'):
                if sec_et.find('title') is not None:
                    sec_title_et = sec_et.find('title')

                if sec_et.find('p') is not None:
                    p_et = sec_et.find('p')
                    # print(p_et.text)

                    getValue(p_et)

                    # p = "".join(p_et.text + str([et.tostring(e, encoding='unicode') for e in list(p_et)]))
                    # sec_title = "".join(str([sec_title_et.text] + [et.tostring(e) for e in sec_title_et.getchildren()]))

                    # print(p)
            # print(secs)
except et.ParseError as error:
    print(error)

