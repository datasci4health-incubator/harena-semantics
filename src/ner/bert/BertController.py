from .bert import Ner
# from .biobert_pytorch import Ner

# from src.ner.bert.Bert import Ner

import os

class BertController:
    def predict(self, text):
        # model = Ner("/app/src/ner/bert/pretrained_models/enzo_model/")
        # model = Ner("/app/src/ner/bert/pretrained_models/biobert_pytorch")
        model = Ner("/app/src/ner/bert/pretrained_models/BC5CDR-IOB")



        output = model.predict(text)
        print(output)
        return output
