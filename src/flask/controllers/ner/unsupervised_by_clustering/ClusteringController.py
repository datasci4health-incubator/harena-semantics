# from .clustring import Ner
# from .dist_v2 import BertEmbeds
from .clusterer import BertEmbeds

# from .biobert_pytorch import Ner

# from src.ner.bert.Bert import Ner

import os

class ClusteringController:
    def predict(self, text):
        

        DIR = "src/flask/controllers/ner/unsupervised_by_clustering/"
        model = BertEmbeds('bert-large-cased',0, DIR+'vocab.txt', DIR+'bert_vectors.txt',False,True,DIR+'results/labels.txt',DIR+'results/stats_dict.txt',DIR+'preserve_1_2_grams.txt',DIR+'glue_words.txt')
# retorna as top 10 entidades que representam o texto como um todo (mas principalmente, o termo que é definido como o pivot)

        output = model.find_entities(text.split())
        print('cluster output: ',output)

        return output
