import requests
import xml.etree.ElementTree as et

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"

params = dict(db='pubmed', retmode='xml', rettype='MEDLINE')


# print(r.text)


def get_pubtype_and_mesh(pmids):
    result = []
    slice_lengths = len(pmids) // 16

    count = 0
    chunks = [pmids[x:x + slice_lengths] for x in range(0, len(pmids), slice_lengths)]

    for chunk in chunks:
        params.update({'id': chunk})
        r = requests.get(url=BASE_URL, params=params, stream=True)
        articles_et = et.fromstring(r.text)

        # print(articles_et)
        for article_et in articles_et:
            pub_types = []
            mesh_terms = []
            if article_et.find("MedlineCitation/PMID") is not None:
                pmid = article_et.find("MedlineCitation/PMID").text

            for pub_type_et in article_et.findall("MedlineCitation/Article/PublicationTypeList/PublicationType"):
                pub_types.append(pub_type_et.text)

            for mesh_term_et in article_et.findall("MedlineCitation/MeshHeadingList/MeshHeading/DescriptorName"):
                mesh_terms.append(mesh_term_et.text)

            result.append( { 'pmid':pmid, 'types':pub_types, 'mesh_terms':mesh_terms} )
        return result

# get_pubtype_and_mesh(i)
#
# data = r.json()
# print(data)
# # result = HttpClient.get(query);
