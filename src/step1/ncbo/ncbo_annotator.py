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

    def highlights_mesh(self, text):
        params.update({'text': text})
        r = requests.post(url=BASE_URL, params=params, stream=True, headers={'Authorization': 'apikey token=' + API_KEY})

        result_array = json.loads(r.text)
        # print(result_array)
        new_text = ""
        excerpts = []
        i = 0

        for x in result_array:
            annotations = x.get('annotations')
            count = 0
            for y in annotations:
                mesh_term = y.get('text')
                print(mesh_term)

                from_index = y.get('from')
                to_index = y.get('to')

                excerpt = text[i:from_index-1] + '{' + text[from_index-1:to_index] + '}'
                excerpts.append(excerpt)
                i = to_index
                count = count + 2

        # print(new_texts)
        for e in excerpts:
            new_text = new_text + e
        print(excerpts)
        return new_text

# print(jsonArray)