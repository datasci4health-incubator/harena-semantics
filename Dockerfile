FROM python:3.7

ENV PIN_PIPENV_VERSION=2021.5.29

RUN pip install --upgrade --no-cache-dir pipenv

# Defining working directory and adding source code
WORKDIR /app
COPY ./src/flask .
# COPY Pipfile Pipfile.lock bootstrap.sh ./

# Install API dependencies
RUN pipenv --python 3.7
RUN pipenv install

## Start app
#EXPOSE 10040
ENTRYPOINT ["./bootstrap.sh"]
