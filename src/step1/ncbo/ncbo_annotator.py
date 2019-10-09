import requests, json

BASE_URL = "http://data.bioontology.org/annotator"
API_KEY = '1cff5532-d88d-4a43-97a2-729e43dd2a4b'
params = dict(ontologies='MESH',
              exclude_numbers='true',
              exclude_synonyms='false',
              longest_only='true')


def get_mesh_terms(text):
    params.update({'text': text})
    r = requests.post(url=BASE_URL, params=params, stream=True, headers={'Authorization': 'apikey token=' + API_KEY})

    resultArray = json.loads(r.text)
    mesh_terms = []

    for x in resultArray:
        annotations = x.get('annotations')
        for y in annotations:
            mesh_terms.append(y.get('text'))
    return mesh_terms

# print(jsonArray)