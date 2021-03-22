from .bert import Ner
# from .biobert_pytorch import Ner

# from src.ner.bert.Bert import Ner

import os

class BertController:
    def predict(self, text):
        # model = Ner("/app/src/ner/bert/pretrained_models/enzo_model/")
        # model = Ner("/app/src/ner/bert/pretrained_models/biobert_pytorch")
        # pretrained_model = "/app/src/ner/bert/pretrained_models/BC5CDR-IOB"
        # pretrained_model = "/app/src/ner/bert/pretrained_models/biobert_ner"
        model = "/app/models/word_embeddings/BC5CDR-IOB"

        # print('pretrained_model', pretrained_model)
        model = Ner(model)


        output = model.predict(text)
        print(output)
        return output
