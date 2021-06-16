# Base NLP spaCy

## Install the NLP spaCy tool locally

```bash
pip install git+ssh://git@git.contexity.com:10379/sccn/nlp-interface.git
pip install -U conllu textacy pyyaml
python -m spacy download en_core_web_md
python -m spacy download de_core_news_md
```

**Important**

Do not install spacy with ```pip install -U spacy```, because that would install version 3.x leading to version conflicts

The reason is that textacy already installed spacy 2.3.5, as it does not work with newer versions of spacy:
<https://github.com/chartbeat-labs/textacy#L52>

## Usage

Start the tool

```bash
python -m tool -port 8080
```

and then open your browser <http://localhost:8080/spacy/api-docs/>

## Build and run the docker image

```bash
sudo docker build -t spacy .
sudo docker run -p 8080:8080 --name spacy -d spacy
```

and then open your browser <http://localhost:8080/spacy/api-docs/>