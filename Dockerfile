# Using alpine image
FROM python:3.7-alpine

# Installing packages
RUN apk update
RUN pip install --no-cache-dir pipenv

# Defining working directory and adding source code
WORKDIR /app
COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY src ./src

# Install API dependencies
RUN pipenv install pysolr

## Start app
EXPOSE 5000
ENTRYPOINT ["./bootstrap.sh", "initialseeder.py"]




