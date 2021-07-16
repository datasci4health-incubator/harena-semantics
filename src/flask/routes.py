import sys, os, logging, pdb
import requests
# import pysolr
import pandas as pd
import xml.etree.ElementTree as et

from pathlib import Path
from flask import Flask, render_template, jsonify, request
from collections import Counter

from controllers.ner.ncbo.ncbo_annotator import Annotator
from controllers.ner.bern.BernController import BernController
from controllers.ner.bert.BertController import BertController
from controllers.ner.unsupervised_by_clustering.ClusteringController import ClusteringController
# from src.experiments.first.workflow import perform
# from src.pos.PoSController import PoSController
# from src.embeddings.EmbeddingController import EmbeddingController

# import tensorflow as tf

app = Flask(__name__)
app.run(debug=True)


@app.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return render_template('index.html')


#################
# NER services #
#################
#################
@app.route('/ner/ncbo', methods=['POST'])
def ncbo():
    text = request.form.get('text')
    ontologies = request.form.get('ontologies')
    whole_word_only = request.form.get('whole_word_only')
    exclude_numbers = request.form.get('exclude_numbers')
    exclude_synonyms = request.form.get('exclude_synonyms')
    longest_only = request.form.get('longest_only')
    expand_mappings = request.form.get('expand_mappings')
    semantic_types = request.form.get('semantic_types')

    a = Annotator(ontologies,
                    whole_word_only,
                    exclude_numbers,
                    exclude_synonyms,
                    longest_only,
                    expand_mappings,
                    semantic_types)

    return jsonify(a.highlights_mesh(text))


@app.route('/ner/bern', methods=['POST'])
def bern():
    text = request.form.get('text')
    bern = BernController()

    return jsonify(bern.retrieve_ner(text))


@app.route('/ner/bert', methods=['POST'])
def bert():
    text = request.form.get('text')
    bert = BertController()

    bert_output = bert.predict(text)
    # bert_output = bert.predict_refactoring(text)

    return jsonify(bert_output)


@app.route('/ner/unsupervised', methods=['POST'])
def clustering():
    text = request.form.get('words')
    cluster = ClusteringController()

    cluster_output = cluster.predict(text)
    return jsonify(cluster_output)
##################################################



##################################################
# indexer services #
##################################################
##################################################
@app.route('/indexer', methods=['GET'])
def indexer_end_point():
    indexer()
    return 'indexed'


@app.route('/searcher', methods=['POST'])
def get_papers():
    print('aqui')

    retrieved_papers = dict()
    titles = []
    description = request.form.get('description')
    mode = request.form.get('mode')

    related_papers = search_by_category(description,
                                          'type:\'randomized controlled trial\' title:randomized abstract:randomized title:placebo abstract:placebo',
                                          mode)

    for paper in related_papers:
        if paper.get('title') is not None:
            titles.append({'title': ''.join(paper.get('title'))})
    retrieved_papers.update({'papers': titles})
    return jsonify(retrieved_papers)
##################################################


@app.route('/exp1', methods=['GET'])
def exp1():
    return jsonify(perform())


##################################################
# Embeddings services #
##################################################
##################################################
@app.route('/embeddings', methods=['GET'])
def get_embeddings():
    text = request.form.get('text')
    result_file = request.form.get('result_file')
    print(len(text))
    embedding_controller = EmbeddingController()
    embedding_controller.create_tsv_files_refactored(text, result_file)
    return "success"


@app.route('/get_masked_embedding', methods=['GET'])
def get_masked_embedding():
    text = request.form.get('text')

    print('------------------- Sentence: ', text)
    embedding_controller = EmbeddingController()
    out = embedding_controller.from_masked_term(text)
    return out


@app.route('/embeddings/similarity', methods=['GET'])
def get_embeddings_similarity():
    tsv_1 = request.form.get('tsv_1')
    tsv_2 = request.form.get('tsv_2')


    tsv_1_dir = 'src/embeddings/tsv_files/' + tsv_1 + '/last_embedding.tsv'
    tsv_label_1_dir = 'src/embeddings/tsv_files/' + tsv_1 + '/labels.tsv'
    tsv_2_dir = 'src/embeddings/tsv_files/' + tsv_2 + '/last_embedding.tsv'
    tsv_label_2_dir = 'src/embeddings/tsv_files/' + tsv_1 + '/labels.tsv'

    tsv1_embeddings_read = pd.read_csv(tsv_1_dir, sep='\t')
    tsv1_labels_read = pd.read_csv(tsv_label_1_dir, sep='\t')

    tsv2_embeddings_read = pd.read_csv(tsv_2_dir, sep='\t')
    tsv2_labels_read = pd.read_csv(tsv_label_2_dir, sep='\t')

    tag_values = list(set(tsv2_labels_read['labels'].values))

    print(type(tsv1_embeddings_read))


    # for embedding_row in tsv1_embeddings_read:
    #     print(len(embedding_row))
        # break

    print(len(tag_values))


    unique_labels = []
    unique_embeddings = []
    for ((index, row), label) in zip(tsv1_embeddings_read.iterrows(), tsv1_labels_read['labels']):
        if label not in unique_labels:
            unique_labels.append(label)
            unique_embeddings.append(row)


    # print(len(unique_labels))
    # print('embeddings ',len(unique_embeddings))

    data=tf.convert_to_tensor(unique_embeddings[0])
    print(type(unique_embeddings))
    print(type(data))
    # print(type(unique_embeddings[0]))

    # preciso retomar a partir daqui. Não consegui ainda fazer cosine().
     # Continuei no notebook gpu-jupyter/harena-asm/tentando comparar dois embeddings
     # lá estou tentando fazer usando tensores, pois nesta imagem não esta funcionando gpu (???) não sei se é issmo mesmo


    return "success"




# Pra estes serviços funcionar é preciso clonar e rodar o repositorio https://github.com/ajitrajasekharan/JPTDP_wrapper
# na subpasta src/pos/JPTDP_wraper
@app.route('/pos', methods=['POST'])
def pos_tagger():
    text = request.form.get('text')

    pos = PoSController()
    pos_list = pos.tags(text)

    return jsonify(pos_list)


@app.route('/graph/concepts', methods=['GET'])
def concept_graph():
    text = request.form.get('text')
    print('------------------- Sentence: ', text)
    pos = PoSController()

    pos_list = pos.tags(text)
    print(pos_list)

    stop = False
    sentences = []

    list_of_nn = []

    while not stop:
        stop = True
        i = 0

        masked = False
        # nn = False
        sentence = ""
        masked_term = ""
        for pos in pos_list:
            word = pos['term']
            if (pos['pos'].startswith("NN")):
                if (pos['term'] not in list_of_nn):
                    # print ("Element Exists")
                    list_of_nn.append(pos['term'])
                if not pos['masked'] and not masked:

                    word = "entity"
                    pos['masked'] = True
                    masked = True
                    stop = False
                    masked_term = pos['term']


            sentence += word + " "
        sentences.append({ 'sentence': sentence, 'masked_word': masked_term })

    sentences.pop()
    print('list_of_nn ----------------------', list_of_nn)

    list_of_fully_predictions = ""
    embedding_controller = EmbeddingController()


    for sentence in sentences:
        print('Masked Word: ', sentence['masked_word'])
        out = embedding_controller.from_masked_term(sentence['sentence'])
        sentence['predictions'] = out
        list_of_fully_predictions += out
        print('Predictions', out,"\n\n")
        break
    # print('oooooooooooooooout', out)

    embedding_controller.create_tsv_files(list_of_fully_predictions)
    return jsonify(list_of_fully_predictions)


@app.route('/graph/nn_concepts', methods=['GET'])
def concept_nn_graph():
    text = request.form.get('text')
    print('------------------- Sentence: ', text)
    pos = PoSController()

    pos_list = pos.tags(text)
    # print(pos_list)

    list_of_nn = []
    sentence_terms = ""

    for pos in pos_list:
        word = pos['term']
        if (pos['pos'].startswith("NN")):
            print()
            sentence_terms += pos['term']
            list_of_nn.append(pos['term'])

    embedding_controller = EmbeddingController()
    embedding_controller.create_tsv_files(sentence_terms)

    return('resultado')
    # result = Counter(list_of_nn)
    # result2 = sorted(result.items(), key=lambda i: i[1], , reverse=True)
    # result2 = result.most_common()
    # df = pd.DataFrame.from_dict(result2, orient='index').reset_index()
    # df.to_csv("src/embeddings/tsv_files/nns.tsv", index=False, sep="\t")


    # return jsonify(result2)
    # POS_SERVICE_URL = "http://127.0.0.1:8028/"
    # response = requests.get(url=POS_SERVICE_URL + text)
    #
    # rows = str(response.text).split('\n')
    #
    # pos_dict = []
    #
    # for row in rows:
    #     columns = row.split('\t')
    #
    #     if len(columns) == 5:
    #         pos_dict.append({ columns[1]: columns[2] })
    #         # pos_dict[int(columns[0])] =
    #
    # return jsonify(pos_dict)
# if __name__ == '__main__':
#     app.run(debug=True)
