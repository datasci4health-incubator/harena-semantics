import requests, json

import re

class BernController:


    def retrieve_ner(self, text):
        # Uncomment when production env
        # url='https://bern.korea.ac.kr/plain'
        # response = requests.post(url, data={'sample_text': text}).json()

        # when is development env, i'll we a file instead call bern service in order to prevent so many requests
        # comment this when at production
        with open('src/ner/bern/bern_response_example.json') as json_file:
            data = json.load(json_file)
            response = data

        diseases = response['logits']['disease']

        annotations = []

        # each disease is [ {id, start, end}, float]
        for disease in diseases:
            start = disease[0]['start']
            end = disease[0]['end']

            annotation = '{{ ' + text[start:end] + ' }}'

            context_annotation = (annotation, (start, end))
            annotations.append(context_annotation)

        print(annotations)

        i = 0
        for annotation in annotations:
            start = annotation[1][0] + (i * 6)
            end = annotation[1][1] + (i * 6)

            text = text[0:start] + annotation[0] + text[end:]

            i+= 1

        return text
