# from .bert import Ner
# from .biobert_pytorch import Ner

# from src.ner.bert.Bert import Ner
# from pytorch_transformers import *
import torch

from transformers import BertForMaskedLM, BertModel
from transformers import BertTokenizer

import pdb
import os
import numpy as np
from collections import OrderedDict
import pandas as pd
import csv
from collections import Counter

from torch import Tensor

from src.ner.bert.bert import Ner


def read_descs(file_name):
    ret_dict = {}
    with open(file_name) as fp:
        line = fp.readline().rstrip("\n")
        if (len(line) >= 1):
            ret_dict[line] = 1
        while line:
            line = fp.readline().rstrip("\n")
            if (len(line) >= 1):
                ret_dict[line] = 1
    return ret_dict


class SingletonEmbeddingController(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class EmbeddingController(metaclass=SingletonEmbeddingController):
    def __init__(self):
        # MODEL_PATH ='bert-large-cased'
        # MODEL_PATH='dmis-lab/biobert-base-cased-v1.1'
        #
        # MODEL_PATH = 'monologg/biobert_v1.1_pubmed'
        MODEL_PATH = "/app/models/BC5CDR-IOB"

        # self.model = Ner("/app/src/ner/bert/pretrained_models/BC5CDR-IOB")


        self.model = BertModel.from_pretrained(MODEL_PATH, output_hidden_states = True)
        self.model.train()
        # self.model = BertForMaskedLM.from_pretrained(MODEL_PATH)
        # self.model = BertModel.from_pretrained(MODEL_PATH, output_hidden_states = True)

        self.tokenizer = BertTokenizer.from_pretrained(MODEL_PATH,do_lower_case=False)


        DESC_FILE="src/embeddings/common_descs.txt"
        self.descs = read_descs(DESC_FILE)
        self.top_k = 40


    def get_hidden_states(self, marked_text):
        tokenized_text = self.tokenizer.tokenize(marked_text)
        indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)

        segments_ids = [1] * len(tokenized_text)

        tokens_tensor = torch.tensor([indexed_tokens])
        segments_tensors = torch.tensor([segments_ids])

        with torch.no_grad():
            outputs = self.model(tokens_tensor, segments_tensors)
            hidden_states = outputs[2]
            return hidden_states

    def get_hidden_states_refactored(self, marked_text):
        tokenized_text = self.tokenizer.tokenize(marked_text)
        indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)

        segments_ids = [1] * len(tokenized_text)

        tokens_tensor = torch.tensor([indexed_tokens])
        segments_tensors = torch.tensor([segments_ids])


        with torch.no_grad():
            outputs = self.model(tokens_tensor, segments_tensors)
            # print('type',outputs.shape)
            hidden_states = outputs[2]
            return hidden_states

    def get_embeddings(self, text):
        marked_text = "[CLS] " + text + " [SEP]"

        hidden_states = self.get_hidden_states(marked_text)
        token_embeddings = torch.stack(hidden_states, dim=0)
        token_embeddings = torch.squeeze(token_embeddings, dim=1)
        token_embeddings = token_embeddings.permute(1,0,2)

        return token_embeddings


    def get_embeddings_refactored(self, text):
        marked_text = "[CLS] " + text + " [SEP]"

        hidden_states = self.get_hidden_states_refactored(marked_text)
        token_embeddings = torch.stack(hidden_states, dim=0)
        token_embeddings = torch.squeeze(token_embeddings, dim=1)
        token_embeddings = token_embeddings.permute(1,0,2)

        return token_embeddings

    def create_tsv_files_refactored(self, text, result_file):
        tokenized_input = self.tokenizer.tokenize(text)
        last_embeddings = []

        for token in tokenized_input:
            token_embeddings = self.get_embeddings_refactored(token)
            last_embedding_layer = token_embeddings[1][12]

            tsv_rows = ''
            for e in last_embedding_layer:
                tsv_rows += str(e.item()) + '\t'
            last_embeddings.append(tsv_rows)

            # TRYING TO WORK WITH panda
            # pandas_rows = []

            # pandas_columns = []
            # for e in last_embedding_layer:
            #     pandas_columns.append(e.item())
            # pandas_rows.append(pandas_columns)

        # df = pd.DataFrame(data=pandas_rows)
        # print(df)
        # pd.DataFrame(df).to_csv('src/embeddings/tsv_files/' + result_file + '/last_embedding_pandas' )


        column_index = ""
        for i in range(0,768):
            column_index += str(i) + '\t'
        print(column_index)

        PATH_DIR = 'src/embeddings/tsv_files/' + result_file + '/'

        if not os.path.exists(PATH_DIR):
            os.mkdir(PATH_DIR)

        with open(PATH_DIR + 'last_embedding.tsv', "w") as f:
            print(column_index, file=f)
            for e in last_embeddings:
                print (e, file=f)


        with open(PATH_DIR + "labels.tsv", "w") as labels_file:
            print('labels', file=labels_file)
            for token in tokenized_input:
                print(token, file=labels_file)


    def create_tsv_files(self, list_of_fully_predictions):
        tokenized_input = self.tokenizer.tokenize(list_of_fully_predictions)
        tokenized_input_pd = pd.Index(tokenized_input)

        token_counts = tokenized_input_pd.value_counts()
        token_indexes = token_counts.keys()

        first_embeddings = []
        last_embeddings = []
        valid_tokens_indexes = []
        valid_tokens_counts = []

        i = 0

        for token in tokenized_input:
            if (not token.startswith("##") or token.startswith("##")):
                i= i + 1
                marked_text = "[CLS] " + token + " [SEP]"

                valid_tokens_indexes.append(token)
                valid_tokens_counts.append(token_counts[token])

                token_embeddings = self.get_embeddings(marked_text)


                # first_embedding_layer = token_embeddings[1][1]
                last_embedding_layer = token_embeddings[1][12]

                tsv_rows = ''
                for e in last_embedding_layer:
                    tsv_rows += str(e.item()) + '\t'
                last_embeddings.append(tsv_rows)

                # tsv_rows = ''
                # for e in first_embedding_layer:
                #     tsv_rows += str(e.item()) + '\t'
                # first_embeddings.append(tsv_rows)

        # with open("src/embeddings/tsv_files/artigos_sepsis/first_embedding.tsv", "w") as f:
        #     for e in first_embeddings:
        #         print('saving')
        #         print (e, file=f)
        # print('saved')
        with open("src/embeddings/tsv_files/artigos_sepsis/last_embedding.tsv", "w") as f:
            for e in last_embeddings:
                print (e, file=f)


        # data = {'wotttrd':  valid_tokens_indexes,
        #         'count': valid_tokens_counts
        #        }
        data_tuples = list(zip(valid_tokens_indexes,valid_tokens_counts))
        df = pd.DataFrame(data_tuples)
        df.to_csv("src/embeddings/tsv_files/artigos_sepsis/labels.tsv", index=False, sep="\t")


    def create_nns_file(self, list_of_nn):
        list_of_nn_pd = pd.Index(list_of_nn)
        result = Counter(list_of_nn)
        print(result)
        print(list_of_nn_pd)
        token_counts = list_of_nn_pd.value_counts()

        data_tuples = list(zip(list_of_nn,token_counts))
        df = pd.DataFrame(data_tuples)
        # df.to_csv("src/embeddings/tsv_files/nns.tsv", index=False, sep="\t")

        token_indexes = token_counts.keys()
        # print(token_counts)
        # print(token_indexes)
        return result

    def from_masked_term(self, text):
        # print('------------------------------------------ text')
        # print(text)
        # print(len(text))
        text = '[CLS]' + text + '[SEP]'
        tokenized_text = self.tokenizer.tokenize(text)
        indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)

        # Create the segments tensors.
        segments_ids = [0] * len(tokenized_text)

        masked_index = 0
        original_masked_index = 0
    #     print('id ', id)
    #     print(text[id])
    #     tokenized_text[id] = "entity"
        for i in range(len(tokenized_text)):
            if (tokenized_text[i] == "entity"):
                masked_index = i
                original_masked_index = i
                break
        # print('tokenized_text ',tokenized_text)
        #assert (masked_index != 0)
        if (masked_index == 0):
            return "Specify and input sentence with the term entity in it. This word will be masked"
        tokenized_text[masked_index] = "[MASK]"
        indexed_tokens[masked_index] = 103
    #     print('tokenized_text', tokenized_text)
    #     print('masked_index ',masked_index)
        results_dict = {}

        # Convert inputs to PyTorch tensors
        tokens_tensor = torch.tensor([indexed_tokens])
        segments_tensors = torch.tensor([segments_ids])

        ret_str = ""
        mask_str = ""
        debug_str = "\nPIVOT_DESCRIPTORS:"
        delimiter_str = "\n--------Neighbors for all words in sentence below (including MASK word)-----\n\n"
        head_str ="\nTokenized input:" +  ' '.join(tokenized_text) + "\n\n"
        elements = ""


        with torch.no_grad():
            predictions = self.model(tokens_tensor, segments_tensors)


            for word in range(len(tokenized_text)):
                if (word == 0 or word == len(tokenized_text) -1):
                    continue
                masked_index = word


                ret_str += "\n\n" + str(word) + ") Neighbors for word: "  + tokenized_text[word] + "\n"
                if (original_masked_index == word):
                    mask_str += "\n\n" + str(word) + ") Neighbors for word: "  + tokenized_text[word] + "\n"
                arr = np.array(predictions[0][0][masked_index].tolist())

                mean = np.mean(arr)
                std = np.std(arr)
                min_val = np.min(arr)
                max_val = np.max(arr)
                hist,bins = np.histogram(arr,bins = [-50,-18,-16,-14,-12,-10,-8,-6,-4,-2,0,2,4,6,8,10,12,14,16,18,50])

                #hist,bins = np.histogram(arr,bins = [-20,-16,-12,-8,-4,0,4,8,12,16,20])
                if (original_masked_index == word):
                    mask_str += "Stats:" + " mean: " + str(mean) + " std: " + str(std) + " max: " + str(max_val) + " min: " + str(min_val)  +"\n"

                ret_str += "Stats:" + " mean: " + str(mean) + " std: " + str(std) + " max: " + str(max_val) + " min: " + str(min_val)  +"\n"
                bin_str = ""
                assert len(bins) == len(hist) + 1
                for bin_index in range(len(bins)):
                    if (bin_index < len(hist)):
                        bin_str +=  " [" + str(bins[bin_index]) + " to " + str(bins[bin_index+1]) + ") :" + str(hist[bin_index]) + "\n"
                    #else:
                    #    bin_str +=  " " + str(bins[bin_index])
                #hist_str = ""
                #for hist_index in range(len(hist)):
                #    hist_str +=  " " + str(hist[hist_index])
                if (original_masked_index == word):
                    mask_str += "Bins-counts:\n" +  bin_str + "\n"



                ret_str += "Bins-counts:\n" +  bin_str + "\n"
                #ret_str += "Hist: " + str(hist_str) + "\n"
                for i in range(len(predictions[0][0][masked_index])):
                    tok = self.tokenizer.convert_ids_to_tokens([i])[0]
                    results_dict[tok] = float(predictions[0][0][masked_index][i].tolist())
                k = 0


                sorted_d = OrderedDict(sorted(results_dict.items(), key=lambda kv: kv[1], reverse=True))
                # print('sorted_ddddddddddddddddddddddddddddddddddd ', sorted_d)
                # if (original_masked_index == word):
                #     print(len(tokenized_text))
                #     print('predictions ', (predictions, type(predictions[0]), predictions[0].shape ))
                #     print('embedding of ', (word, arr, type(arr), len(arr)))

                debug_count = 0
                for j in sorted_d:
    #                 print('j ', j)
                    if (j not in self.descs):
                        continue
                    if (original_masked_index == word):
                        elements += j + " "
                        mask_str = mask_str + str(k+1) + "] " +  j + " " + str(sorted_d[j]) + "\n"
                        if (debug_count < 10):
                            debug_str  = debug_str + " " + j
                            debug_count += 1

    #                 print(sorted_d[j])
                    ret_str = ret_str + str(k+1) + "] " +  j + " " + str(sorted_d[j]) + "\n"

                    k += 1
                    if (k >= self.top_k):
                        break
        # print(head_str + "\n"  + mask_str + debug_str + "\n")
        # +   delimiter_str + ret_str)
        # return head_str + "\n"  + mask_str + debug_str + "\n" +   delimiter_str + ret_str
        # pdb.set_trace()
        # print('head_str iiiiiiiiiiiiiiiii',head_str)
        # print('---------------------------- ', mask_str)
        # return (head_str + "\n"  + mask_str)
        # print(elements)


        return elements


    def pytorch_cos_sim(a: Tensor, b: Tensor):
        """
        Computes the cosine similarity cos_sim(a[i], b[j]) for all i and j.
        This function can be used as a faster replacement for 1-scipy.spatial.distance.cdist(a,b)
        :return: Matrix with res[i][j]  = cos_sim(a[i], b[j])
        """
        if not isinstance(a, torch.Tensor):
            a = torch.tensor(a)

        if not isinstance(b, torch.Tensor):
            b = torch.tensor(b)

        if len(a.shape) == 1:
            a = a.unsqueeze(0)

        if len(b.shape) == 1:
            b = b.unsqueeze(0)

        a_norm = a / a.norm(dim=1)[:, None]
        b_norm = b / b.norm(dim=1)[:, None]
        return torch.mm(a_norm, b_norm.transpose(0, 1))
