import connexion
import six
from flask import Flask
import json
from openapi_server import util
from openapi_server.services.analysis import *

# When the server starts, load all the available language models in a dictionary
# (dictionary's format explained inside the function)
nlp_models = load_nlp_models()

def text_to_conllu(text, lang='de', comments=None):  # noqa: E501
    """Get dependency analysis for a text, in CoNLL-U format

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
    """

    # Use convert_text_to_conllu of the analysis module
    conllu = convert_text_to_conllu(text, lang, nlp_models, comments)

    return conllu, 200


def text_to_graph(text, lang='de'):  # noqa: E501
    """Get dependency analysis for a text

    Get dependency analysis for a text, as a dependency graph, by providing text and language # noqa: E501

    :param text: The text that will be subjected to dependency analysis
    :type text: str
    :param lang: The language of the text
    :type lang: str

    :rvalue dep_graph: The dependency graph as an svg image (svg+xml format)
    :rtype: str
    """

    # Use convert_text_to_graph of the analysis module    
    dep_graph = convert_text_to_graph(text, lang, nlp_models)
    
    return dep_graph, 200

def conllu_to_graph(body):  # noqa: E501
    """Get dependency analysis given a CoNLL-U format

    Get dependency analysis for a text by providing its already known CoNLL-U format # noqa: E501

    :param body: The conllu table corresponding to a text
    :type body: str

    :rvalue dep_graph: The dependency graph as an svg image (svg+xml format)
    :rtype: str
    """

    # Use convert_conllu_to_graph of the analysis module 
    dep_graph = convert_conllu_to_graph(body)
    
    return dep_graph, 200