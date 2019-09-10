import requests, json

BASE_URL = "http://data.bioontology.org/annotator"
API_KEY = '1cff5532-d88d-4a43-97a2-729e43dd2a4b'
params = dict(text='A 58-year-old African-American woman presents to the ER with episodic pressing/burning anterior chest pain that began two days earlier for the first time in her life. The pain started while she was walking, radiates to the back, and is accompanied by nausea, diaphoresis and mild dyspnea, but is not increased on inspiration. The latest episode of pain ended half an hour prior to her arrival. She is known to have hypertension and obesity. She denies smoking, diabetes, hypercholesterolemia, or a family history of heart disease. She currently takes no medications. Physical examination is normal. The EKG shows nonspecific changes.',
              ontologies='MESH',
              exclude_numbers='true',
              exclude_synonyms='false',
              longest_only='true')

r = requests.post(url=BASE_URL, params=params, stream=True, headers={'Authorization': 'apikey token=' + API_KEY})

jsonArray = json.loads(r.text)

for x in jsonArray:
    print(x.get('annotations'))
    print()

# print(jsonArray)