import requests, json

BASE_URL = "http://data.bioontology.org/annotator"
API_KEY = '1cff5532-d88d-4a43-97a2-729e43dd2a4b'
params = dict(ontologies='MESH',
              exclude_numbers='true',
              exclude_synonyms='false',
              longest_only='true')

class Annotator:

    def get_mesh_terms(self, text):
        params.update({'text': text})
        r = requests.post(url=BASE_URL, params=params, stream=True, headers={'Authorization': 'apikey token=' + API_KEY})

        resultArray = json.loads(r.text)
        mesh_terms = []
        for x in resultArray:
            annotations = x.get('annotations')
            for y in annotations:
                mesh_terms.append(y.get('text'))
        return mesh_terms


    def sort_by_index(self, result_array):
        meshs = []

        for result_element in result_array:
            irl = result_element.get("annotatedClass").get('@id')
            annotations = result_element.get('annotations')

            for y in annotations:
                from_index = y.get('from')
                to_index = y.get('to')

                mesh_json = {'irl':irl, 'from_index':from_index, 'to_index':to_index}
                meshs.append(mesh_json)
        meshs.sort(key=lambda x: x['from_index'])
        return meshs


    def highlights_mesh(self, text):
        params.update({'text': text})
        r = requests.post(url=BASE_URL, params=params, stream=True, headers={'Authorization': 'apikey token=' + API_KEY})

        result_array = json.loads(r.text)

        meshs = self.sort_by_index(result_array)

        new_text = ""
        excerpts = []
        i = 0
        for element in meshs:
            excerpt = text[i:element['from_index'] - 1] + '{' + text[element['from_index'] - 1:element['to_index']] + '}'
            excerpts.append(excerpt)

            i = element['to_index']

        for e in excerpts:
            new_text = new_text + e
        new_text = new_text + text[element['to_index']:]

        print(excerpts)

        return (new_text, meshs)

# print(jsonArray)