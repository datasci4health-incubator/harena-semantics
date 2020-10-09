from flask import Flask, render_template, jsonify, request

import pysolr, os
import logging, sys
import xml.etree.ElementTree as et

from src.experiments.first.workflow import perform
from src.solr_functions import indexer, search_by_category, indexMESH
from src.ncbo.ncbo_annotator import Annotator
from src.pubmed.entrez_utilities import get_pubtype_and_mesh

app = Flask(__name__)


@app.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return render_template('index.html')


@app.route('/searcher', methods=['POST'])
def get_papers():
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

@app.route('/indexer', methods=['GET'])
def indexer_end_point():
    indexer()
    return 'indexed'


@app.route('/indexMESH', methods=['POST'])
def indexer_end_point2():
    indexMESH()
    return 'indexed'


@app.route('/exp1', methods=['GET'])
def exp1():
    return jsonify(perform())


@app.route('/annotate', methods=['POST'])
def annotate():
    text = request.form.get('text')
    a = Annotator()

    return jsonify(a.highlights_mesh(text))


@app.route('/ner', methods=['POST'])
def ner():
    text = request.form.get('text')
    bern = BernController()

    return jsonify(bern.retrieve_ner(text))
