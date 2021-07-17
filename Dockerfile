FROM python:3.6

RUN pip install --no-cache-dir pipenv

# Defining working directory and adding source code
WORKDIR /app
COPY ./src/flask .
# COPY Pipfile Pipfile.lock bootstrap.sh ./

# Install API dependencies
RUN pipenv install

## Start app
#EXPOSE 10040
ENTRYPOINT ["./bootstrap.sh"]
