import requests


class BernController:


    def retrieve_ner(self, text):
        url='https://bern.korea.ac.kr/plain'

        response = requests.post(url, data={'sample_text': text}).json()
        print('logits')
        logits = response['logits']

        diseases = logits['disease']

        print(diseases)

        return diseases
