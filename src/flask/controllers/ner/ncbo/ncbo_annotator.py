import requests, json, os
# import pysolr
from flask import jsonify

BASE_URL = "http://data.bioontology.org/annotator"
API_KEY = '1cff5532-d88d-4a43-97a2-729e43dd2a4b'

class Annotator:
    params = dict(ontologies='MESH',
                  require_exact_match='true')
                  # exclude_numbers='false',
                  # exclude_synonyms='false',
                  # longest_only='false')


    def __init__(self, ontologies, whole_word_only, exclude_numbers, exclude_synonyms, longest_only, expand_mappings, semantic_types):
        self.params.update({'whole_word_only': whole_word_only})
        self.params.update({'ontologies': ontologies})
        self.params.update({'exclude_numbers': exclude_numbers})
        self.params.update({'exclude_synonyms': exclude_synonyms})
        self.params.update({'longest_only': longest_only})
        self.params.update({'expand_mappings': expand_mappings})
        self.params.update({'semantic_types': semantic_types})


    def get_mesh_terms(self, text):
        self.params.update({'text': text})
        r = requests.post(url=BASE_URL, params=self.params, stream=True, headers={'Authorization': 'apikey token=' + API_KEY})

        resultArray = json.loads(r.text)
        mesh_terms = []
        for x in resultArray:
            annotations = x.get('annotations')
            for y in annotations:
                mesh_terms.append(y.get('text'))
        return mesh_terms


    def get_resources(self, xml):
        meshs = []

        for element in xml:
            # print(element)
            # print('------------------------elements------------------')

            irl = element.get("annotatedClass").get('@id')
            ontology = element.get("annotatedClass").get('links').get('ontology')

            annotations = element.get('annotations')

            for y in annotations:
                from_index = y.get('from')
                to_index = y.get('to')
                text = y.get('text')

                mesh_json = {'irl':irl, 'from_index':from_index, 'to_index':to_index, 'text':text, 'ontology':ontology}
                meshs.append(mesh_json)
        meshs.sort(key=lambda x: x['from_index'])
        print(meshs)
        return meshs


    def highlights_mesh(self, input_text):
        self.params.update({'text': input_text})

        r = requests.post(url=BASE_URL, params=self.params, stream=True, headers={'Authorization': 'apikey token=' + API_KEY})

        result_array = json.loads(r.text)
        # print(result_array)
        meshs = self.get_resources(result_array)
        # print('meshs '+str(meshs))

        new_text = ""
        excerpts = []
        i = 0

        index_from_guard = []
        index_to_guard = []
        ontologies_to_guard = []

        for element in meshs:
            if element['from_index'] not in index_from_guard and element['to_index'] not in index_to_guard:
                index_from_guard.append(element['from_index'])
                index_to_guard.append(element['to_index'])
                excerpt = input_text[i:element['from_index'] - 1] + '{' + input_text[element['from_index'] - 1:element['to_index']] + '}(' + element['ontology'].split('/')[-1] + ':' + element['irl'].split('/')[-1] + ')'

                excerpts.append(excerpt)

                i = element['to_index']


                if element['ontology'] not in ontologies_to_guard:
                    ontologies_to_guard.append(element['ontology'])
        for e in excerpts:
            new_text = new_text + e
        new_text = new_text + input_text[element['to_index']:]

        # print('-----------------------------------------------')
        # print(excerpts)

        data_layer = """ \n____ Data _____ \n
                               * theme: jacinto \n
                               * namespaces: \n """
        for o in ontologies_to_guard:
            data_layer  = data_layer + ' * ' + o.split('/')[-1] + ':' + o + ' \n'
                                    # * evidence: http://purl.org/versum/evidence/ \n
                                    # * meddra: http://purl.bioontology.org/ontology/MEDDRA \n
                                    # * ncit: https://bioportal.bioontology.org/ontologies/NCIT"""
        new_text = new_text + data_layer

        # new_text += data_layer

        return new_text

    def get_concept(self, descriptor_id):
        MESH_URL = 'http://' + os.environ['SOLR_HOST'] + ':8983/solr/mesh'


        solr = pysolr.Solr(MESH_URL)
        query = 'DescriptorUI:' + descriptor_id
        concept = solr.search(q=query)

        t = []
        for c in concept:
            if c.get('ConceptName') is not None:
                print(c.get('ConceptName'))
                t.append({'title': ''.join(c.get('ConceptName'))})
        print(jsonify(t))
        return jsonify(t)
# print(jsonArray)
