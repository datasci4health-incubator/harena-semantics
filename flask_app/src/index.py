from flask import Flask, jsonify, request
import pysolr

import logging, sys, os, requests
app = Flask(__name__)

incomes = [
  { 'description': 'salary', 'amount': 5000 }
]


@app.route('/search')
def get_search():
  URL = 'http://'+ os.environ['SOLR_HOST']+':8983/solr/pmc'
  solr = pysolr.Solr(URL, results_cls=dict)
  r = solr.search('title:banana', **{'fl':'title'})
  # logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
  # logging.debug('aquiiiiiiiiiiiiiiiiiiii')

  return r

@app.route('/add')
def add():
  URL = 'http://'+ os.environ['SOLR_HOST']+':8983/solr/pmc'
  solr = pysolr.Solr(URL, results_cls=dict)

  solr.add([
    {
      "id": "doc_1",
      "title": "A test document invocado",
    },
    {
      "id": "doc_2",
      "title": "The avocado: Tasty or Dangerous?",
      "_doc": [
        {"id": "child_doc_1", "title": "peel"},
        {"id": "child_doc_2", "title": "seed"},
      ]
    },
  ])
  return jsonify(incomes)

@app.route('/incomes')
def get_incomes():
  jsonify(incomes)

@app.route('/incomes', methods=['POST'])
def add_income():
  incomes.append(request.get_json())
  return '', 204
