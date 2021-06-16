# imports for dependency analysis
from spacy import displacy
from textacy.export import doc_to_conll
import json
from openapi_server.services.helpers import split_conllu_into_sentences, conll_u_string2displacy_json, remove_comments_in_conllu, concat_displacy_dicts
from openapi_server.error_management.errors import *
import conllu

# import nlp models (they first need to be downloaded from spacy using, e.g.: 
# python -m spacy download en_core_web_sm)
import de_core_news_md
import en_core_web_md

def load_nlp_models():
    """ Load all available languge models

    Load all available language models in a dictionary nlp_models, whose keys are the code names of the
    available languages and whose values are the loaded models for these languages.

    :rvalue nlp_models:
    :rtype: dict

    :Example: Example format of the return value:
    nlp_models = {
        'en': nlp_en_md
        'de': nlp_de_md}
    """

    # Initialize dictionary
    nlp_models = {}

    # Load and store language models
    nlp_models['de'] = de_core_news_md.load()
    nlp_models['en'] = en_core_web_md.load()

    return nlp_models


def convert_text_to_conllu(text, lang, nlp_models, comments=None):
    """ Get dependency analysis for a text, in CoNLL-U format

    Get dependency analysis for a text, in CoNLL-U format, by providing text and language.
    Details about the CoNLL-U format: https://universaldependencies.org/format.html # noqa: E501

    :param text: The text that will be subjected to dependency analysis
    :type text: str
    :param lang: The language of the text
    :type lang: str
    :param comments: Whether to return the CoNLL-U table with comments or not.
    :type comments: bool

    :rvalue conllu: The CoNLL-U table as a string
    :rtype: str

    :Example: Example of a CoNLL-U table that consists of two smaller ones
    "# sent_id 1
    1	This	this	DET	DT	_	2	nsubj	_	_
    2	is	be	AUX	VBZ	_	0	root	_	_
    3	a	a	DET	DT	_	4	det	_	_
    4	sentence	sentence	NOUN	NN	_	2	attr	_	SpaceAfter=No
    5	.	.	PUNCT	.	_	2	punct	_	_

    # sent_id 2
    1	This	this	DET	DT	_	2	nsubj	_	_
    2	is	be	AUX	VBZ	_	0	root	_	_
    3	another	another	DET	DT	_	4	det	_	_
    4	sentence	sentence	NOUN	NN	_	2	attr	_	SpaceAfter=No
    5	.	.	PUNCT	.	_	2	punct	_	SpaceAfter=No"
    """

    # If text is empty, raise an Exception that will return a response 
    # with the proper information about the error
    if len(text)==0:
        raise BadRequestProblem(detail="The 'text' parameter is empty. Cannot return CoNLL-U table for empty string. Please fill the text you'd like to analyze.", type="EMPTY_PARAMETER")

    # Choose the right model based on the "lang" argument
    nlp_model = nlp_models.get(lang)
    if nlp_model==None:
        raise BadRequestProblem(detail="The 'lang' parameter is not one of those specified in the documentation. Please use one of them.", type="WRONG_PARAMETER")
    
    # Process text (tokens are created)
    doc = nlp_model(text)

    # Convert text to conllu format, using the function doc_to_conll from the textacy library
    # doc_to_conll converts a spaCy doc into a CoNLL-U formatted string
    conllu_string = doc_to_conll(doc)
    
    # Remove the '# sent_id i' from each sentence's conllu-format if comments==None or comments==false
    if comments:
        conllu_string_output = conllu_string
    else:
        conllu_string_output = remove_comments_in_conllu(conllu_string)

    return conllu_string_output


def convert_text_to_graph(text, lang, nlp_models):
    """ Get dependency analysis for a text

    Get dependency analysis for a text, as a dependency graph, by providing text and language # noqa: E501

    :param text: The text that will be subjected to dependency analysis
    :type text: str
    :param lang: The language of the text
    :type lang: str

    :rvalue dep_graph: The dependency graph as an svg image (svg+xml format)
    :rtype: str
    """

    # If text is empty, raise an Exception that will return a response 
    # with the proper information about the error
    if len(text)==0:
        raise BadRequestProblem(detail="The 'text' parameter is empty. Cannot return dependency graph for empty string. Please fill the text you'd like to analyze.", type="EMPTY_PARAMETER")

    # Choose the right model based on the "lang" argument
    nlp_model = nlp_models.get(lang)
    if nlp_model==None:
        raise BadRequestProblem(detail="The 'lang' parameter is not one of those specified in the documentation. Please use one of them.", type="WRONG_PARAMETER")

    # Process text (tokens are created)
    doc = nlp_model(text)
    
    # Build the svg image of the dependency graph
    dep_graph = displacy.render(doc, style="dep", jupyter=False)

    return dep_graph


def convert_conllu_to_graph(body):
    """ Get dependency analysis given a CoNLL-U format

    Get dependency analysis for a text by providing its already known CoNLL-U format

    :param body: The conllu table corresponding to a text
    :type body: str

    :rvalue dep_graph: The dependency graph as an svg image (svg+xml format)
    :rtype: str

    :Example: Example of a CoNLL-U table that consists of two smaller ones
    "# sent_id 1
    1	This	this	DET	DT	_	2	nsubj	_	_
    2	is	be	AUX	VBZ	_	0	root	_	_
    3	a	a	DET	DT	_	4	det	_	_
    4	sentence	sentence	NOUN	NN	_	2	attr	_	SpaceAfter=No
    5	.	.	PUNCT	.	_	2	punct	_	_

    # sent_id 2
    1	This	this	DET	DT	_	2	nsubj	_	_
    2	is	be	AUX	VBZ	_	0	root	_	_
    3	another	another	DET	DT	_	4	det	_	_
    4	sentence	sentence	NOUN	NN	_	2	attr	_	SpaceAfter=No
    5	.	.	PUNCT	.	_	2	punct	_	SpaceAfter=No"
    """

    # If body is empty, raise an Exception that will return a response 
    # with the proper information about the error
    if len(body)==0:
        raise BadRequestProblem(detail="The request body is empty. Cannot return dependency graph for empty CoNLL-U table. Please fill the CoNLL-U table you'd like to analyze.", type="EMPTY_REQUEST_BODY")

    # The request body is in a byte format, when the function is called from the API. We decode it into 'utf-8', before the analysis
    if isinstance(body, bytes):
        conllu_table = body.decode('utf-8')
    else:
        conllu_table = body

    # If conllu_table is not in the right CoNLL-U format, raise an Exception that will return a response
    # with the proper information about the error
    try:
        sentences = conllu.parse(conllu_table)
    except conllu.exceptions.ParseException:
        raise BadRequestProblem(detail="The request body is not in the CoNLL-U format, as expected. Cannot return dependency graph for a wrong format. Please fill a valid string in the request body.", type="WRONG_REQUEST_BODY")

    # Split table into smaller ones; one for each sentence
    splitted_conllu_tables = split_conllu_into_sentences(conllu_table)

    # Convert each CoNLL-U table into a dictionary following DisplaCy's format and store them in a list
    displacy_dicts_list = []
    for table in splitted_conllu_tables:
        displacy_dicts_list.append(json.loads(conll_u_string2displacy_json(table)))

    # Concatenate displacy dicts, in order that the indices of the words in each dictionary don't
    # start from 0 but from the integer that follows the last index of the dictionary of the 
    # sentence preceding the current sentence (more details inside the function)
    whole_displacy_dict = concat_displacy_dicts(displacy_dicts_list)
    
    # Build the svg image of the dependency graph. When manual=True, displacy.render gets as input data in DisplaCy's format instead of 'doc'
    dep_graph = displacy.render(whole_displacy_dict, style="dep", jupyter=False, manual=True)

    return dep_graph

import argparse

if __name__ == "__main__":

    # read arguments from command line
    parser = argparse.ArgumentParser()

    parser.add_argument('--mode', type=str, default='train')