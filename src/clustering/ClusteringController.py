# from .clustring import Ner
from .dist_v2 import BertEmbeds
# from .biobert_pytorch import Ner

# from src.ner.bert.Bert import Ner

import os

class ClusteringController:
    def predict(self, text):

        DIR = "src/clustering/"
        model = BertEmbeds('bert-large-cased',0, DIR+'vocab.txt', DIR+'bert_vectors.txt',True,True,DIR+'results/labels.txt',DIR+'results/stats_dict.txt',DIR+'preserve_1_2_grams.txt',DIR+'glue_words.txt')
        output = model.find_entities(text.split())
        return output
