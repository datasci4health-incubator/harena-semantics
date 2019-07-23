from flask import Flask, jsonify, request
import pysolr, os
import logging, sys
app = Flask(__name__)

incomes = [
  { 'description': 'salary', 'amount': 5000 }
]


@app.route('/incomes')
def get_incomes():
  solr = pysolr.Solr('http://' + os.environ['SOLR_HOST']+':8983/solr/pmc')
  # solr.add([
  #   {
  #     "id": "doc_4",
  #     "title": "A test document",
  #   },
  #   {
  #     "id": "doc_5",
  #     "title": "The Banana: Tasty or Dangerous?",
  #     "_doc": [
  #       {"id": "child_doc_1", "title": "peel"},
  #       {"id": "child_doc_2", "title": "seed"},
  #     ]
  #   },
  # ])
  r = solr.search('seed')
  logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
  logging.debug("Saw {0} result(s).".format(len(r)))
  for r1 in r:
    logging.debug("The title is '{0}'.".format(r1['title']))
  print(r)
  return jsonify(incomes)


@app.route('/incomes', methods=['POST'])
def add_income():
  incomes.append(request.get_json())
  return '', 204
