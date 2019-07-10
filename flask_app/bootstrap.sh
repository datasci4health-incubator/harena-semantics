#!/bin/sh
export FLASK_APP=./src/index.py
export FLASK_ENV=development
source $(pipenv --venv)/bin/activate

if [[ ! -d ../documents ]]; then
    mkdir ../documents/
fi
if [[ ! -d ../documents/pmc ]]; then
    mkdir ../documents/pmc/
fi

if [[ ! -d ../documents/pmc/pmc-text-03 ]]; then
    if [[ ! -e pmc-text-03.tar.gz ]]; then
        wget ceb.nlm.nih.gov/~simpsonmatt/pmc-text-00.tar.gz
        wget ceb.nlm.nih.gov/~simpsonmatt/pmc-text-01.tar.gz
        wget ceb.nlm.nih.gov/~simpsonmatt/pmc-text-02.tar.gz
        wget ceb.nlm.nih.gov/~simpsonmatt/pmc-text-03.tar.gz

        tar xzf pmc-text-00.tar.gz -C ../documents/pmc
        rm pmc-text-00.tar.gz

        tar xzf pmc-text-01.tar.gz -C ../documents/pmc/
        rm pmc-text-01.tar.gz

        tar xzf pmc-text-02.tar.gz -C ../documents/pmc/
        rm pmc-text-02.tar.gz

        tar xzf pmc-text-03.tar.gz -C ../documents/pmc/
        rm pmc-text-03.tar.gz
    fi
fi



flask run -h 0.0.0.0

