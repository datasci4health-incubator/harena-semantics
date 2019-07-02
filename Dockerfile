# Using alpine image
FROM alpine:latest

# Installing packages
RUN apk update
RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip \
    && pip install --no-cache-dir pipenv

# Defining working directory and adding source code
WORKDIR /app
COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY src ./src

# Install API dependencies
RUN pipenv install

# Start app
EXPOSE 5000
ENTRYPOINT ["./bootstrap.sh"]
