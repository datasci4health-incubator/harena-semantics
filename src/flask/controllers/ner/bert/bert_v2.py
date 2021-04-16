import os, json
import numpy as np
import pandas as pd
import pdb

import nltk
from nltk import word_tokenize

import torch
import torch.nn.functional as F
from torch import nn

# from pytorch_transformers import (BertForTokenClassification, BertTokenizer)
from transformers import BertForTokenClassification
from transformers import BertTokenizer

from transformers import (
    AutoConfig,
    AutoModelForTokenClassification,
    # AutoModel,
    AutoTokenizer,
    # EvalPrediction,
    # HfArgumentParser,
    Trainer,
    TrainingArguments,
    # set_seed,
)

from dataclasses import dataclass, field

# from .bert_v2 import Ner

from typing import List, Tuple

from .utils_ner_refact import NerDataset, Split
# from utils_ner_refact import NerDataset, Split, get_labels


class BertNer(BertForTokenClassification):

    def teste(self, input_ids, token_type_ids=None, attention_mask=None, valid_ids=None):
        print('testooooooou')

@dataclass
class DataTrainingArguments:
    """
    Arguments pertaining to what data we are going to input our model for training and eval.
    """

    data_dir: str = field(
        metadata={"help": "The input data dir. Should contain the .txt files for a CoNLL-2003-formatted task."}
    )

    max_seq_length: int = field(
        default=128,
        metadata={
            "help": "The maximum total input sequence length after tokenization. Sequences longer "
            "than this will be truncated, sequences shorter will be padded."
        },
    )
    overwrite_cache: bool = field(
        default=False, metadata={"help": "Overwrite the cached training and evaluation sets"}
    )

class Ner:
    # model_cache_dir/ = ''
    # self.model_cache_dir = None
    def __init__(self,model_dir: str):

        # Mudar depois pro diretorio que quero salvar modelo baixado do huggingface
        self.model_cache_dir = None
        self.use_fast: bool = field(default=False, metadata={"help": "Set this flag to use fast tokenization."})

        self.model , self.tokenizer, self.config = self.load_model(model_dir)

# training_args.do_train

        # print(self.model_cache_dir)
        # comentario do codigo do biobert
        # If you want to tweak more attributes on your tokenizer, you should do it in a distinct script,
        # or just modify its tokenizer_config.json.


        # self.model , self.tokenizer, self.model_config = self.load_model(model_dir)
        # self.label_map = self.model_config["label_map"]
        # self.max_seq_length = self.model_config["max_seq_length"]
        # self.label_map = {int(k):v for k,v in self.label_map.items()}
        # self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # self.model = self.model.to(self.device)
        # self.model.eval()


    def load_model(self, model_dir: str, config_name:str = "config.json"):
        # "Pretrained config name or path if not the same as model_name"
        # print(config_file.id2label

        config_file = os.path.join(model_dir, config_name)
        config_json = json.load(open(config_file))

        # config_json['']

        # print(config_json["id2label"])
        # print(self.model_cache_dir)


        self.config = AutoConfig.from_pretrained(
            # config_name if config_name else model_dir,
            model_dir,

            # num_labels=num_labels,

            id2label=config_json["id2label"],
            label2id=config_json["label2id"],
            cache_dir=self.model_cache_dir,
        )


        self.model = AutoModelForTokenClassification.from_pretrained(
            model_dir,
            from_tf = bool(".ckpt" in model_dir),
            config=self.config,
            cache_dir=self.model_cache_dir,
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            # model_args.tokenizer_name if model_args.tokenizer_name else model_args.model_name_or_path,
            model_dir,


            cache_dir=self.model_cache_dir,
            use_fast=self.use_fast,
        )

        # config_path = os.path.join(model_dir, config_json)
        # print(config_path)
        # config = json.load(open(config_path))
        # model = BertNer.from_pretrained(model_dir)
        # tokenizer = BertTokenizer.from_pretrained(model_dir, do_lower_case=model_config["do_lower"])

        training_args = TrainingArguments
        # Initialize our Trainer
        self.trainer = Trainer(
            model=self.model,
            # args=training_args,
            # train_dataset=train_dataset,
            # compute_metrics=compute_metrics,
            # eval_dataset=eval_dataset,
        )
        return self.model, self.tokenizer, self.config


    def align_predictions(self, predictions: np.ndarray, label_ids: np.ndarray) -> Tuple[List[int], List[int]]:
        # print('predictiooooooooooooooooooons', predictions)
        preds = np.argmax(predictions, axis=2)
        # print('depois do softmax ', preds)
        batch_size, seq_len = preds.shape

        out_label_list = [[] for _ in range(batch_size)]
        preds_list = [[] for _ in range(batch_size)]

        # print('predictions ',predictions)
        for i in range(batch_size):
            for j in range(seq_len):
                if label_ids[i, j] != nn.CrossEntropyLoss().ignore_index:
                    # print('self.config.id2label[label_ids[i][j]] ',self.config.id2label)
                    # print('label_ids[i][j] ',label_ids[i][j])
                    # print(self.config.id2label.get(6))
                    out_label_list[i].append(self.config.id2label.get(label_ids[i][j]))
                    # print('--------------------------------------------------preds')
                    # print(preds)
                    # print(preds[i][j])
                    preds_list[i].append(self.config.id2label[preds[i][j]])
        return preds_list, out_label_list

    def predict_v2(self, text: str):
        # tag_values = ["I-Anatomy", "B-Protein", "B-Cell", "I-Pathology", "B-Organism", "B-Chemical", "I-Gene", "B-Disease",
        #     "I-Organ", "I-Protein", "I-Tissue", "I-Chemical", "I-Taxon", "I-Organism", "I-Disease", "B-Gene", "B-Anatomy",
        #     "B-Tissue", "I-Cell", "I-Cancer", "B-Cancer", "O", "B-Organ", "B-Pathology", "B-Taxon", "PAD"]

        tag_values = ["I-Disease", "O", "I-Chemical", "B-Chemical", "B-Disease", "PAD"]


        tokenized_sentence = self.tokenizer.encode(text)
        input_ids = torch.tensor([tokenized_sentence])

        from torch.utils.data.dataset import Dataset
        print(self.config.id2label.values())

        self.labels = self.config.id2label.values()
        print(self.config.id2label)
        self.labels_list = list(self.config.id2label.values())

        # in_hist = [list(in_degrees.values()).count(x) for x in in_values]

        # label_map: self.config.id2label

        # print('-------------------------')

        # print(self.config.model_dir)
        # for i, label in enumerate(self.config.id2label.values()):
        #     print(i, label)
        # labels = [v: for k, v in self.config.id2label]
        # for v in self.config.id2label:
        #     print(v)

        # labels = get_labels(data_args.labels)

        print(self.labels_list)

        # label_map: Dict[int, str] = {i: label for i, label in enumerate(labels)}
        # print(label_map)
        # num_labels = len(labels)



        test_dataset = NerDataset(
            data_dir=self.config._name_or_path,
            tokenizer=self.tokenizer,
            labels=self.labels_list,
            model_type=self.config.model_type,
            # max_seq_length=data_args.max_seq_length,
            # overwrite_cache=data_args.overwrite_cache,
            mode=Split.test,
        )
        # print(test_dataset[0])
        predictions, label_ids, metrics = self.trainer.predict(test_dataset)

        # print('predictions ', predictions)
        # print('label_ids ', label_ids)
        # print('metrics ', metrics)

        preds = np.argmax(predictions, axis=2)
        print('after softmax ', preds)


        print('pfvvvvvvvvvvvvvvvvvvv')
        # print(predictions)
        # print('label_idskkkkkkkkkkkkkkkkkkkkkkkkk ',label_ids[0][1])
        # print(self.config.id2label.get(label_ids[0][1]))
        # print(self.config.label2id)
        # print(self.config.label2id.get(3))
        # print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', self.labels_list[1])
        # print(label_ids)
        # print('iiiiiiiiiiiiiiiiiiiiiiiiiiii')

        labels_new=[]
        for l_id in label_ids:
            print(l_id)
            for l_l_id in l_id:
                # print('???????????????????????????????/')
                # print(l_l_id)
                if l_l_id == -100:
                    # print('PAD')
                    labels_new.append('PAD')
                else:
                    # print()
                    labels_new.append(self.labels_list[l_l_id])
        print(labels_new)


        # print(self.labels_list)
        # self.
        # label_ids
        # preds_list, _ = self.align_predictions(predictions, label_ids)

        # print('seeeeeeeeeeeeeeeeera')
        # print(preds_list)
        # print(_)
        # print(preds_list)
        # Save predictions
        # output_test_results_file = os.path.join(training_args.output_dir, "test_results.txt")
        # # if trainer.is_world_master():
        # with open(output_test_results_file, "w") as writer:
        #     logger.info("***** Test results *****")
        #     for key, value in metrics.items():
        #         logger.info("  %s = %s", key, value)
        #         writer.write("%s = %s\n" % (key, value))
        #
        # output_test_predictions_file = os.path.join(training_args.output_dir, "test_predictions.txt")
        # # if trainer.is_world_master():
        # with open(output_test_predictions_file, "w") as writer:
        #     with open(os.path.join(data_args.data_dir, "test.txt"), "r") as f:
        #         example_id = 0
        #         for line in f:
        #             if line.startswith("-DOCSTART-") or line == "" or line == "\n":
        #                 writer.write(line)
        #                 if not preds_list[example_id]:
        #                     example_id += 1
        #             elif preds_list[example_id]:
        #                 entity_label = preds_list[example_id].pop(0)
        #                 if entity_label == 'O':
        #                     output_line = line.split()[0] + " " + entity_label + "\n"
        #                 else:
        #                     output_line = line.split()[0] + " " + entity_label[0] + "\n"
        #                 # output_line = line.split()[0] + " " + preds_list[example_id].pop(0) + "\n"
        #                 writer.write(output_line)
        #             else:
        #                 logger.warning(
        #                     "Maximum sequence length exceeded: No prediction for '%s'.", line.split()[0]
        #                 )





        # self.trainer.predict(test_dataset)

        # with torch.no_grad():
        #     # trainer.predict(input_ids)
        #     output = self.model(input_ids)
        # print('zeros',output[0].to('cpu').numpy())
        #
        # label_indices = np.argmax(output[0].to('cpu').numpy(), axis=2)
        # print(label_indices)
        # # join bpe split tokens
        # tokens = self.tokenizer.convert_ids_to_tokens(input_ids.to('cpu').numpy()[0])
        # new_tokens, new_labels = [], []
        #
        versum = ""
        # for idx, (token, label_idx) in enumerate(zip(tokens, label_indices[0])):
        #     if (token == "[CLS]" or token == "[SEP]"):
        #         continue
        #
        #     # print(tag_values[label_indices[0][idx+1]][0])
        #     next = tag_values[label_indices[0][idx+1]][0]
        #     next_b = tag_values[label_indices[0][idx+1]].startswith("B")
        #
        #     if (tag_values[label_idx] == "O"):
        #         if token.startswith("##"):
        #             # se o proximo começa com ##
        #             if (tokens[idx + 1].startswith("##")):
        #                 versum += token[2:]
        #             else:
        #                 versum += token[2:] + " "
        #         else:
        #             if (tokens[idx + 1].startswith("##")):
        #                 versum += token
        #             else:
        #                 versum += token + " "
        #
        #     if (tag_values[label_idx].startswith("B")):
        #         if next == "O":
        #             # este if so existe por causa de outputs como d(B-disease) ##ys(B-disease) ##p(B-disease) ##nea(B-disease)
        #             # acredito que esse caso não deveria existir, e deve ser resultado de erro no treinamento do modelo.
        #             # estou registrando este erro como: Erro 1
        #             if token.startswith("##"):
        #                 versum += token[2:] + "}(" + tag_values[label_idx][2:] + ") "
        #             else:
        #                 # sem o erro bastaria esta linha, sem o if
        #                 versum += "{" + token + "}(" + tag_values[label_idx][2:] + ") "
        #
        #         if next == "I":
        #             versum += "{" + token
        #         if next == "B":
        #             # Consequencia do Erro 1
        #             if token.startswith("##"):
        #                 versum += token[2:]
        #             else:
        #                 # sem o erro bastaria esta linha, sem o ir
        #                 versum += "{" + token
        #     if (tag_values[label_idx].startswith("I")):
        #         if next == "O":
        #             versum += " " + token + "}(" + tag_values[label_idx][2:] + ") "
        #         if next == "I":
        #             versum += " " + token

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
