# Using alpine image
FROM solr:latest

# Installing packages
USER root

RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip

RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir pipenv
RUN pip install Flask

# Defining working directory and adding source code
USER solr

WORKDIR /app
COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY src ./src

USER root
# Install API dependencies
RUN pipenv install
USER solr


# Start app
EXPOSE 5000
ENTRYPOINT ["./bootstrap.sh"]




