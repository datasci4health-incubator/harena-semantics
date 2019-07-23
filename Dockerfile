# Using alpine image
FROM python:3.7

# Installing packages
#RUN apk update
RUN pip install --no-cache-dir pipenv
RUN pip install --upgrade setuptools

# Defining working directory and adding source code
WORKDIR /app/flask_app

# Install API dependencies
RUN pipenv install pysolr spacy

## Start app
EXPOSE 5000
ENTRYPOINT ["./bootstrap.sh"]




