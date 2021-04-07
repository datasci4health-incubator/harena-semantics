import requests, json

import re

class BernController:


    def retrieve_ner(self, text):
        # Uncomment when production env
        url='https://bern.korea.ac.kr/plain'
        response = requests.post(url, data={'sample_text': text}).json()


    # When in development env, i'll use a file instead call bern service in order to prevent so many requests
    # Comment this when at production
        # with open('src/ner/bern/bern_response_example.json') as json_file:
        #     data = json.load(json_file)
        #     response = data


        print(response)
        denotations = response['denotations']
        annotations = []

        for denotation in denotations:
            obj = denotation['obj']
            start = denotation['span']['begin']
            end = denotation['span']['end']

            annotation = '{' + text[start:end] +'}('+ obj + ')'
            extra_chars = len(annotation) - len(text[start:end])
            context_annotation = (annotation, (start, end, extra_chars))
            annotations.append(context_annotation)

        print(annotations)

        i = 0
        for annotation in annotations:
            start = annotation[1][0] + i
            end = annotation[1][1] + i

            text = text[0:start] + annotation[0] + text[end:]
            i+= annotation[1][2]

        return text
