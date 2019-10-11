from flask import Flask, jsonify, request
import pysolr, os
import logging, sys
import xml.etree.ElementTree as et

from src.experiments.first.workflow import perform
from src.step1.searcher import Searcher
from src.step1.ncbo.ncbo_annotator import Annotator

app = Flask(__name__)

@app.route('/searcher', methods=['POST'])
def get_papers():
  retrieved_papers = dict()
  titles = []
  description = request.form.get('description')
  mode = request.form.get('mode')

  s = Searcher()
  related_papers = s.search_by_category(description, 'type:\'randomized controlled trial\' title:randomized abstract:randomized title:placebo abstract:placebo', mode)

  for paper in related_papers:
    if paper.get('title') is not None:
      titles.append({'title':''.join(paper.get('title'))})
  retrieved_papers.update({'papers':titles})
  return jsonify(retrieved_papers)

@app.route('/exp1', methods=['GET'])
def exp1():
  return jsonify(perform())

@app.route('/annotate', methods=['POST'])
def annotate():
    text = request.form.get('text')
    a = Annotator()

    return jsonify(a.highlights_mesh(text))