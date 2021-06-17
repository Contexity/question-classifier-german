FROM python:3.9-slim

RUN apt-get update
RUN apt-get install -y build-essential git

RUN pip install -U conllu textacy==0.10.1
RUN python -m spacy download en_core_web_md
RUN python -m spacy download de_core_news_md

WORKDIR /usr/src/app
RUN mkdir logs
COPY . /usr/src/app
RUN pip install /usr/src/app/nlp-interface

EXPOSE 8080
ENV SERVICE_PORT=8080

CMD python3 -m tool -port ${SERVICE_PORT}