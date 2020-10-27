from .bert import Ner
# from src.ner.bert.Bert import Ner

import os

class BertController:
    def predict(self, text):
        model = Ner("/app/src/ner/bert/biobert_out_base/")
        output = model.predict(text)
        print(output)
        return output
