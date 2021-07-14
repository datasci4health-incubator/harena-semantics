import os, json
import numpy as np
import pandas as pd
import pdb

import nltk
from nltk import word_tokenize

import torch
import torch.nn.functional as F

# from pytorch_transformers import (BertForTokenClassification, BertTokenizer)
from transformers import BertForTokenClassification
from transformers import BertTokenizer

class BertNer(BertForTokenClassification):

    def teste(self, input_ids, token_type_ids=None, attention_mask=None, valid_ids=None):
        print('testooooooou')


class Ner:
    def __init__(self, model_dir: str):
        self.model , self.tokenizer, self.model_config = self.load_model(model_dir)
        self.label_map = self.model_config["label_map"]
        self.max_seq_length = self.model_config["max_seq_length"]
        self.label_map = {int(k):v for k,v in self.label_map.items()}
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)
        self.model.eval()


    def load_model(self, model_dir: str, model_config: str = "model_config.json"):
        model_config = os.path.join(model_dir,model_config)
        model_config = json.load(open(model_config))
        model = BertNer.from_pretrained(model_dir)
        tokenizer = BertTokenizer.from_pretrained(model_dir, do_lower_case=model_config["do_lower"])

        return model, tokenizer, model_config


    def predict(self, text: str):
        # tag_values = ["I-Anatomy", "B-Protein", "B-Cell", "I-Pathology", "B-Organism", "B-Chemical", "I-Gene", "B-Disease",
        #     "I-Organ", "I-Protein", "I-Tissue", "I-Chemical", "I-Taxon", "I-Organism", "I-Disease", "B-Gene", "B-Anatomy",
        #     "B-Tissue", "I-Cell", "I-Cancer", "B-Cancer", "O", "B-Organ", "B-Pathology", "B-Taxon", "PAD"]


        tag_values = ["I-Disease", "O", "I-Chemical", "B-Chemical", "B-Disease", "PAD"]

        tokenized_sentence = self.tokenizer.encode(text)

        input_ids = torch.tensor([tokenized_sentence],device=self.device)

        with torch.no_grad():
            output = self.model(input_ids)
        # print(output)


        label_indices = np.argmax(output[0].to('cpu').numpy(), axis=2)

        # join bpe split tokens
        tokens = self.tokenizer.convert_ids_to_tokens(input_ids.to('cpu').numpy()[0])
        new_tokens, new_labels = [], []


        versum = ""
        for idx, (token, label_idx) in enumerate(zip(tokens, label_indices[0])):
            if (token == "[CLS]" or token == "[SEP]"):
                continue


            # print(tag_values[label_indices[0][idx+1]][0])
            next = tag_values[label_indices[0][idx+1]][0]
            next_b = tag_values[label_indices[0][idx+1]].startswith("B")

            if (tag_values[label_idx] == "O"):
                if token.startswith("##"):
                    # se o proximo começa com ##
                    if (tokens[idx + 1].startswith("##")):
                        versum += token[2:]
                    else:
                        versum += token[2:] + " "
                else:
                    if (tokens[idx + 1].startswith("##")):
                        versum += token
                    else:
                        versum += token + " "

            if (tag_values[label_idx].startswith("B")):
                if next == "O":
                    # este if so existe por causa de outputs como d(B-disease) ##ys(B-disease) ##p(B-disease) ##nea(B-disease)
                    # acredito que esse caso não deveria existir, e deve ser resultado de erro no treinamento do modelo.
                    # estou registrando este erro como: Erro 1
                    if token.startswith("##"):
                        versum += token[2:] + "}(" + tag_values[label_idx][2:] + ") "
                    else:
                        # sem o erro bastaria esta linha, sem o if
                        versum += "{" + token + "}(" + tag_values[label_idx][2:] + ") "

                if next == "I":
                    versum += "{" + token
                if next == "B":
                    # Consequencia do Erro 1
                    if token.startswith("##"):
                        versum += token[2:]
                    else:
                        # sem o erro bastaria esta linha, sem o ir
                        versum += "{" + token
            if (tag_values[label_idx].startswith("I")):
                if next == "O":
                    versum += " " + token + "}(" + tag_values[label_idx][2:] + ") "
                if next == "I":
                    versum += " " + token

        print(versum)
        # pdb.set_trace()
        return versum

    def tokenize(self, text: str):
        """ tokenize input"""
        nltk.download('punkt')

        words = word_tokenize(text)

        tokens = []
        valid_positions = []
        for i,word in enumerate(words):
            token = self.tokenizer.tokenize(word)
            tokens.extend(token)
            for i in range(len(token)):
                if i == 0:
                    valid_positions.append(1)
                else:
                    valid_positions.append(0)
        return tokens, valid_positions


    def preprocess(self, text: str):
        """ preprocess """
        tokens, valid_positions = self.tokenize(text)
        ## insert "[CLS]"
        tokens.insert(0,"[CLS]")
        valid_positions.insert(0,1)
        ## insert "[SEP]"
        tokens.append("[SEP]")
        valid_positions.append(1)
        segment_ids = []
        for i in range(len(tokens)):
            segment_ids.append(0)
        input_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        input_mask = [1] * len(input_ids)
        while len(input_ids) < self.max_seq_length:
            input_ids.append(0)
            input_mask.append(0)
            segment_ids.append(0)
            valid_positions.append(0)
        return input_ids,input_mask,segment_ids,valid_positions
