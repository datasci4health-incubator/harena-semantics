#!/bin/sh
export FLASK_APP=./src/index.py
export FLASK_ENV=development
source $(pipenv --venv)/bin/activate

#pip install spacy
python -m spacy download en_core_web_sm

flask run -h 0.0.0.0
