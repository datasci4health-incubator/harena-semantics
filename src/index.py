from flask import Flask, jsonify, request
import pysolr, os
import logging, sys
import xml.etree.ElementTree as et

from src.experiments.first.workflow import perform

from src.step1.searcher import Searcher
app = Flask(__name__)

incomes = [
  { 'description': 'salary', 'amount': 5000 }
]


@app.route('/incomes')
def get_incomes():
  solr = pysolr.Solr('http://' + os.environ['SOLR_HOST']+':8983/solr/pmc')
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

@app.route('/searcher', methods=['GET'])
def get_papers():
  s = Searcher()
  related_papers = s.search_by_category('chest pain', 'type:\'randomized controlled trial\' title:randomized abstract:randomized title:placebo abstract:placebo')
  retrieved_papers = dict()
  titles = []
  for paper in related_papers:
    if paper.get('title') is not None:
      titles.append({'title':''.join(paper.get('title'))})
  retrieved_papers.update({'papers':titles})
  return jsonify(retrieved_papers)


@app.route('/exp1', methods=['GET'])
def exp1():
  return jsonify(perform())
  # print('foi tudo')
  # return {'a':'a'}