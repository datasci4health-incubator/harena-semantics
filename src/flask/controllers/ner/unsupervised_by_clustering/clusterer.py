import pdb
import sys
import operator
from collections import OrderedDict
import subprocess
import numpy as  np
import json
import math
from transformers import *
import sys
import random


SINGLETONS_TAG  = "_singletons_ "
EMPTY_TAG = "_empty_ "
OTHER_TAG = "OTHER"
AMBIGUOUS = "AMB"

BERT_TERMS_START=106
UNK_ID = 100
#Original setting for cluster generation.
OLD_FORM=True

try:
    from subprocess import DEVNULL  # Python 3.
except ImportError:
    DEVNULL = open(os.devnull, 'wb')



def read_embeddings(embeds_file):
    with open(embeds_file) as fp:
        embeds_dict = json.loads(fp.read())
    return embeds_dict

def read_labels(labels_file):
    terms_dict = OrderedDict()
    with open(labels_file) as fin:
        count = 1
        for term in fin:
            term = term.strip("\n")
            term = term.split()
            if (len(term) == 5):
                terms_dict[term[2]] = {"label":term[0],"aux_label":term[1],"mean":float(term[3]),"variance":float(term[4])}
                count += 1
            else:
                print("Invalid line:",term)
                assert(0)
    print("count of labels in " + labels_file + ":", len(terms_dict))
    return terms_dict


def read_terms(terms_file):
    terms_dict = OrderedDict()

    with open(terms_file) as fin:
        count = 1
        for term in fin:
            term = term.strip("\n")
            if (len(term) >= 1):
                terms_dict[term] = count
                count += 1
    print("count of tokens in ",terms_file,":", len(terms_dict))
    return terms_dict





def is_filtered_term(key): #Words selector. skiping all unused and special tokens
    if (OLD_FORM):
        return True if (str(key).startswith('#') or str(key).startswith('[')) else False
    else:
        return True if (str(key).startswith('[')) else False

def filter_2g(term,preserve_dict):
    if (OLD_FORM):
        return True if  (len(term) <= 2 ) else False
    else:
        return True if  (len(term) <= 2 and term not in preserve_dict) else False

class BertEmbeds:
    def __init__(self, model_path,do_lower, terms_file,embeds_file,cache_embeds,normalize,labels_file,stats_file,preserve_2g_file,glue_words_file):
        do_lower = True if do_lower == 1 else False
        print('chamoooooooooooooooooou')
        print(model_path)
        self.tokenizer = BertTokenizer.from_pretrained(model_path,do_lower_case=do_lower)
        print(self.tokenizer)
        self.terms_dict = read_terms(terms_file)
        self.labels_dict = read_labels(labels_file)
        self.stats_dict = read_terms(stats_file)
        self.preserve_dict = read_terms(preserve_2g_file)
        self.gw_dict = read_terms(glue_words_file)
        self.embeddings = read_embeddings(embeds_file)
        self.cache = cache_embeds
        self.embeds_cache = {}
        self.cosine_cache = {}
        self.dist_threshold_cache = {}
        self.normalize = normalize

    def find_entities(self,words):
        entities = self.labels_dict
        # print('possible entities -----------------------', entitiesz)
        #
        tokenize = False
        words = self.filter_glue_words(words)

        desc_max_term,desc_mean,desc_std_dev,s_dict = self.find_pivot_subgraph(words,tokenize)
        # s_dict é o dicionário ordenado de pivots (termos mais conectados a todos os outros) para essa sentença
        # print("PSG score of input descs:",desc_max_term,desc_mean,desc_std_dev,s_dict)
        #OVERRIDE pivot
        #desc_max_term = words[0]
        #print("pivot override",desc_max_term)
        pivot_similarities = {}
        print('max termmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm', desc_max_term)
        # entities are the 6110 clusteres, que podem ou não estar rotulados
        for i,key in enumerate(entities):
            term = key

            # calcula a similaridade (distancia ??) entre o pivot da sentença e os pivots de cada cluster
            val = round(self.calc_inner_prod(desc_max_term,term,tokenize),2)
            # print(desc_max_term,term,val)
# pivot_similarities são as similaridades entre o pivor e todas as entities pre-definidas
            pivot_similarities[key] = val

            #print("SIM:",desc_max_term,term,val)
# sorte_d é o pivot similaridades ordenado
        sorted_d = OrderedDict(sorted(pivot_similarities.items(), key=lambda kv: kv[1], reverse=True))
        # print(sorted_d)
        count = 0
        ret_arr = []
        # print(len(sorted_d))


        # iterar sobre as top 10 entidades mais similares ao pivot
        for k in sorted_d:
            #if (sorted_d[k] < pick_threshold):
            #    if (count == 0):
            #        print("No entity above thresold")
            #    break
            # print(entities[k]["label"],k,sorted_d[k],"(",entities[k]["mean"],entities[k]["variance"],")")
# entities são os 6 mil clusters, presentes no aquivo results/labels.txt
            # print('entity ',entities[k])
            # verifica se a label é uma das 49 labels contidas em results/stats_dict.txt q foi previamente gerado
#             se tiver a label, então ele marca como OTHER-label (label é o )
            ret_label = self.gen_label(entities[k])
            # print('ret_label ', ret_label)
            # print(ret_label)
            ret_arr.append(ret_label)
            count+= 1
            if (count >= 10):
                break
        # print(ret_arr)
        # print(' e é isto')
        # print
        return ret_arr


    #given n terms, find the mean of the connection strengths of subgraphs considering each term as pivot.
    #return the mean of max strength term subgraph
    # Itera pelos termos de entrada, e controi um grafo conectanto cada termo i com todos os termos j
    # Quando o termo não esta no vocabulario, ele não busca o embedding (isso que tokenize=False faz)
    # ele simplesmente pega o embedding[100] que é unused99. Quando o calc_inner_prod retorna 1.0
    # significa que comparou duas palavras fora do vocabulario do bert
    def find_pivot_subgraph(self,terms,tokenize):
        max_mean = 0
        std_dev = 0
        max_mean_term = None
        means_dict = {}
        if (len(terms) == 1):
            return terms[0],1,0,{terms[0]:1}
        for i in terms:
            full_score = 0
            count = 0
            full_dict = {}
            for j in terms:
                if (i != j):

                    val = self.calc_inner_prod(i,j,tokenize)
                    # if (i=='woman'):
                    #     # print('i: ', i)
                    #     # print('j: ', j)
                    #     # print(val)
                    #     print(i+"-"+j,val)
                    #     print()
                    full_score += val
                    full_dict[count] = val
                    count += 1

            if (len(full_dict) > 0):
                # if (i=='woman'):
                #     print('full_dict :',full_dict)

# Tira uma media de todos do inner_prod(i, j)
                mean  =  float(full_score)/len(full_dict)
                means_dict[i] = mean

                # if (i=='woman'):
                #     print('mean ',mean)
                #print(i,mean)
                if (mean > max_mean):
                    #print("MAX MEAN:",i)
                    max_mean_term = i
                    max_mean = mean
                    std_dev = 0
                    for k in full_dict:
                        std_dev +=  (full_dict[k] - mean)*(full_dict[k] - mean)
                    std_dev = math.sqrt(std_dev/len(full_dict))
                    #print("MEAN:",i,mean,std_dev)
        #print("MAX MEAN TERM:",max_mean_term)
        # print('means_dict ',means_dict)
        # print('woman: ',means_dict['woman'])
        sorted_d = OrderedDict(sorted(means_dict.items(), key=lambda kv: kv[1], reverse=True))
        return max_mean_term,round(max_mean,2),round(std_dev,2),sorted_d


    def calc_inner_prod(self,text1,text2,tokenize):
        # np.set_printoptions(threshold=np.inf)

        if (self.cache and text1 in self.cosine_cache and text2 in self.cosine_cache[text1]):
            return self.cosine_cache[text1][text2]
        if (text1 == 'woman'):
            print('text1', text1)

        vec1 = self.get_embedding(text1,tokenize)
        vec2 = self.get_embedding(text2,tokenize)

        if (vec1 is None or vec2 is None):
            #print("Warning: at least one of the vectors is None for terms",text1,text2)
            return 0
        val = np.inner(vec1,vec2)
        if (text1 == 'woman'):
            print(text1 + ' e ' + text2)
            print('vec1 ',vec1[:])
            print('vec2 ', vec2[:])
            print(val)

        if (self.cache):
            if (text1 not in self.cosine_cache):
                self.cosine_cache[text1] = {}
            self.cosine_cache[text1][text2] = val
        return val

    def get_embedding(self,text,tokenize=True):
        # tokenize = True


        # if text == 'dyspnea,':
        #     print('aquiii ', text)
        if (self.cache and text in self.embeds_cache):
            # if text == 'dyspnea,':
            #     print('está no cache')
            #     print(self.cache)
            #     print(self.embeds_cache[text])

            return self.embeds_cache[text]
        if (tokenize):
            tokenized_text = self.tokenizer.tokenize(text)
        else:
            # if text == 'dyspnea,':
            #     print('texttttttttttttttttttttttttt ', text)
            if (not text.startswith('[')):
               tokenized_text = text.split()
               # if text == 'dyspnea,':
               #     print(tokenized_text)
            else:
               tokenized_text = [text]

        # if text == 'dyspnea,':
        #     print('tokenized_text ', tokenized_text)
        indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)
        # if text == 'dyspnea,':
        #     print('indexed_tokenssssssssssssssssssssssssss ',indexed_tokens)
        vec =  self.get_vector(indexed_tokens)
        if (self.cache):
                self.embeds_cache[text] = vec
        return vec


    def get_vector(self,indexed_tokens):
        vec = None
        if (len(indexed_tokens) == 0):
            return vec
        #pdb.set_trace()
        for i in range(len(indexed_tokens)):
            term_vec = self.embeddings[indexed_tokens[i]]
            if (vec is None):
                vec = np.zeros(len(term_vec))
            vec += term_vec
        sq_sum = 0
        for i in range(len(vec)):
            sq_sum += vec[i]*vec[i]
        sq_sum = math.sqrt(sq_sum)
        for i in range(len(vec)):
            vec[i] = vec[i]/sq_sum
        #sq_sum = 0
        #for i in range(len(vec)):
        #    sq_sum += vec[i]*vec[i]
        return vec


    def filter_glue_words(self,words):
        ret_words = []
        for dummy,i in enumerate(words):
            if (i not in self.gw_dict):
                ret_words.append(i)
        if (len(ret_words) == 0):
            ret_words.append(words[0])
        return ret_words


    def gen_label(self,node):
        print(node)
        if (node["label"] in self.stats_dict):
            print(1)
            if (node["aux_label"] in self.stats_dict):
                ret_label = node["label"] + "-" +  node["aux_label"]
            else:
                if (node["label"]  == AMBIGUOUS):
                    ret_label = node["label"] + "-" +  node["aux_label"]
                else:
                    ret_label = node["label"]
        else:
            print(2)
            ret_label = OTHER_TAG + "-" + node["label"]
        return ret_label
