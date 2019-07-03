# Using alpine image
FROM solr:latest

# Installing packages
RUN apt update \
    && sudo apt install python3-pip

RUN pip install --no-cache-dir pipenv 

# Defining working directory and adding source code
WORKDIR /app
COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY src ./src

# Install API dependencies
RUN pipenv install

# Start app
EXPOSE 5000
ENTRYPOINT ["./bootstrap.sh"]
