#!/bin/bash

export FLASK_APP=./routes.py
export FLASK_ENV=development
export MODEL=ACD

source $(pipenv --venv)/bin/activate

python controllers/ner/bert/download_model.py

# if [[ ! -d ./models ]]; then
#     mkdir ./models/
# fi

  # wget ceb.nlm.nih.gov/~simpsonmatt/pmc-text-00.tar.gz
  #

# if [[ ! -d ./documents ]]; then
#     mkdir ./documents/
# fi
# if [[ ! -d ./documents/pmc ]]; then
#     mkdir ./documents/pmc/
# fi
#
# if [[ ! -d ./documents/pmc/pmc-text-03 ]]; then
#     if [[ ! -e pmc-text-03.tar.gz ]]; then
#         wget ceb.nlm.nih.gov/~simpsonmatt/pmc-text-00.tar.gz
#         wget ceb.nlm.nih.gov/~simpsonmatt/pmc-text-01.tar.gz
#         wget ceb.nlm.nih.gov/~simpsonmatt/pmc-text-02.tar.gz
#         wget ceb.nlm.nih.gov/~simpsonmatt/pmc-text-03.tar.gz
#
#

#         tar xzf pmc-text-00.tar.gz -C ./documents/pmc
#         rm pmc-text-00.tar.gz
#
#         tar xzf pmc-text-01.tar.gz -C ./documents/pmc/
#         rm pmc-text-01.tar.gz
#
#         tar xzf pmc-text-02.tar.gz -C ./documents/pmc/
#         rm pmc-text-02.tar.gz
#
#         tar xzf pmc-text-03.tar.gz -C ./documents/pmc/
#         rm pmc-text-03.tar.gz
#     fi
# fi

# python -m spacy download en_core_web_sm

flask run -h 0.0.0.0
