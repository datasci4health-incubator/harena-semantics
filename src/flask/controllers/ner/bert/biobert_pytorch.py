import os, json
import numpy as np
import pandas as pd
import pdb

# import nltk
# from nltk import word_tokenize

import torch
import torch.nn.functional as F

# from pytorch_transformers import (BertForTokenClassification, BertTokenizer)
from transformers import BertForTokenClassification
from transformers import BertTokenizer


from typing import  List, Tuple

from transformers import (
    AutoConfig,
    AutoModelForTokenClassification,
    EvalPrediction,
    HfArgumentParser,
    Trainer,
    TrainingArguments,
    set_seed,
)

class BertNer(AutoModelForTokenClassification):

    def teste(self, input_ids, token_type_ids=None, attention_mask=None, valid_ids=None):
        print('testooooooou')


class Ner:
    def __init__(self, MODEL_PATH: str):
        self.tokenizer = BertTokenizer.from_pretrained(MODEL_PATH, do_lower_case=False)
        self.config = AutoConfig.from_pretrained(MODEL_PATH)

        self.labels = [value for k, value in self.config.id2label.items()]

        self.model = BertForTokenClassification.from_pretrained(MODEL_PATH,
            num_labels=len(self.labels),
            output_attentions = False,
            output_hidden_states = False
        )
        # self.device = "cuda" if torch.cuda.is_available() else "cpu"


    def predict(self, text: str):
        tokenized_sentence = self.tokenizer.encode(text)

        input_ids = torch.tensor([tokenized_sentence])

        with torch.no_grad():
            output = self.model(input_ids)

        label_indices = np.argmax(output[0].to('cpu').numpy(), axis=2)

        tokens = self.tokenizer.convert_ids_to_tokens(input_ids.to('cpu').numpy()[0])
        new_tokens, new_labels = [], []
        versum = ""

        entitying = False
        change_of_label = False
        current_label = ""
        print(self.config.id2label)
        print(label_indices[0])
        for idx, (token, label_idx) in enumerate(zip(tokens, label_indices[0])):
        #     print(token)
        #     print(label_idx)
        #     print(labels[label_idx])
        #     print()

            if (token == "[CLS]" or token == "[SEP]"):
                continue


            if token.startswith("##"):
                sub_token = True
                versum += token[2:]
                # versum += "".join(token[2:])

            else:
                if (self.labels[label_idx].startswith("B")):
                    if entitying:
                        versum += '}(' + entity +')'
                        # versum = " ".join([versum, '}(' + entity +')'])

                    entitying = True
                    versum += ' {' + token
                    # versum = " ".join([versum, ' {' + token])

                    entity = self.labels[label_idx][2:]

                if self.labels[label_idx].startswith("O") :
                    if entitying:
                        versum += '}(' + entity +') ' + token
                        # versum = " ".join([versum, '}(' + entity +') ' + token])

                    else:
                        versum += ' ' + token
                        # versum = " ".join([versum, token])

                    entitying = False


                if self.labels[label_idx].startswith("I") :
                    if previous_label[2:] != self.labels[label_idx][2:]:
                        versum += '}(' + entity +') {'
                        # versum = " ".join([versum, '}(' + entity +') {'])

                        entity = self.labels[label_idx][2:]
                        change_of_label = True
                    else: change_of_label = False
                    if change_of_label:
                        versum += token
                        # versum = " ".join([versum, token])

                        entitying = True
                    else:
                        entitying = True
                        versum += ' ' + token
                        # versum = " ".join([versum, token])


            previous_label = self.labels[label_idx]





# if token.startswith("##"):
#     sub_token = True
#     versum += "".join(token[2:])
#     # versum = versum + token[2:]
# else:
#     if (self.labels[label_idx].startswith("B")):
#         if entitying:
#             versum = " ".join([versum, '}(' + entity +')'])
#
#         entitying = True
#         versum = " ".join([versum, ' {' + token])
#         entity = self.labels[label_idx][2:]
#
#     if self.labels[label_idx].startswith("O") :
#         if entitying:
#             versum = " ".join([versum, '}(' + entity +') ' + token])
#         else:
#             versum = " ".join([versum, token])
#         entitying = False
#
#     if self.labels[label_idx].startswith("I") :
#         if previous_label[2:] != self.labels[label_idx][2:]:
#             versum = " ".join([versum, '}(' + entity +') {'])
#             entity = self.labels[label_idx][2:]
#             change_of_label = True
#         else: change_of_label = False
#         if change_of_label:
#             versum = " ".join([versum, token])
#             entitying = True
#         else:
#             entitying = True
#             versum = " ".join([versum, token])
#
# previous_label = self.labels[label_idx]





        print(versum)
        return versum
