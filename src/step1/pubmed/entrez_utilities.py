import requests
import xml.etree.ElementTree as et

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"

params = dict(db='pubmed', retmode='xml', rettype='MEDLINE')


# print(r.text)


def get_pubtype_and_mesh(pmid):
    params.update({'id': pmid})
    r = requests.get(url=BASE_URL, params=params)
    article_et = et.fromstring(r.text)

    pub_types = []
    mesh_terms = []

    for pub_type_et in article_et.findall("PubmedArticle/MedlineCitation/Article/PublicationTypeList/PublicationType"):
        pub_types.append(pub_type_et.text)

    for mesh_term_et in article_et.findall("PubmedArticle/MedlineCitation/MeshHeadingList/MeshHeading/DescriptorName"):
        mesh_terms.append(mesh_term_et.text)

    result = { 'types':pub_types, 'mesh_terms':mesh_terms}

    return result


print(get_pubtype_and_mesh(31348278))
#
# data = r.json()
# print(data)
# # result = HttpClient.get(query);
