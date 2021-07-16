# from .bert_v2 import Ner
from .biobert_pytorch import Ner

# from src.ner.bert.Bert import Ner

import os

class BertController:
    def predict(self, text):
        # model = Ner("/app/src/ner/bert/pretrained_models/enzo_model/")
        # model = Ner("/app/src/ner/bert/pretrained_models/biobert_pytorch")
        # pretrained_model = "/app/src/ner/bert/pretrained_models/BC5CDR-IOB"
        # pretrained_model = "/app/src/ner/bert/pretrained_models/biobert_ner"
        # model = "/app/models/word_embeddings/BC5CDR-IOB"
        # print('aqi')
        # MODEL_PATH = "/app/models/ACD(overfited)"
        MODEL_PATH = 'fagner/envoy'

        print('pretrained_model', MODEL_PATH)
        model = Ner(MODEL_PATH)

        output = model.predict(text)

        return output

    MODEL_DIR = "/app/models/word_embeddings/fine_tuned/NER/ACD_1epoch"


    def predict_v2(self, text):
        # model = Ner("/app/src/ner/bert/pretrained_models/enzo_model/")
        # model = Ner("/app/src/ner/bert/pretrained_models/biobert_pytorch")
        # pretrained_model = "/app/src/ner/bert/pretrained_models/BC5CDR-IOB"
        # pretrained_model = "/app/src/ner/bert/pretrained_models/biobert_ner"
        # model = "/app/models/word_embeddings/BC5CDR-IOB"


        # print('pretrained_model', pretrained_model)
        model = Ner(self.MODEL_DIR)


        output = model.predict_v2(text)
        # print(output)
        return output
