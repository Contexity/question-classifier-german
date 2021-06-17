import connexion
import sys
from openapi_server import util

import logging
logger = logging.getLogger(__name__)

try: 
    from tool.services import analysis
except:
    logger.error("Unexpected error: "+str(sys.exc_info()))


def get_conllu_to_graph(conllu):  # noqa: E501
    """Get dependency analysis given a CoNLL-U format

    Get dependency analysis for a text by providing its already known CoNLL-U format # noqa: E501

    :param conllu: The conllu table corresponding to a text
    :type conllu: str

    :rtype: str
    """
    
    # Use convert_conllu_to_graph of the analysis module 
    try: 
        from tool.services import analysis
    except:
        logger.error("Unexpected error: "+str(sys.exc_info()))
        return "", 500
    else:
        logger.debug("Using analysis to return the result of conllu_to_graph")
        dep_graph = analysis.convert_conllu_to_graph(conllu)
        return dep_graph, 200


def get_text_to_conllu(text, lang='de', comments=None):  # noqa: E501
    """Get dependency analysis for a text, in CoNLL-U format

    Get dependency analysis for a text, in CoNLL-U format, by providing text and language # noqa: E501

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
    try: 
        from tool.services import analysis
    except:
        logger.error("Unexpected error: "+str(sys.exc_info()))
        return "", 500
    else:
        logger.debug("Using analysis to return the result of text_to_conllu")
        conllu = analysis.convert_text_to_conllu(text, lang, comments)
        return conllu, 200


def get_text_to_graph(text, lang='de'):  # noqa: E501
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
    try: 
        from tool.services import analysis
    except:
        logger.error("Unexpected error: "+str(sys.exc_info()))
        return "", 500
    else:
        logger.debug("Using analysis to return the result of text_to_graph")
        dep_graph = analysis.convert_text_to_graph(text, lang)
        return dep_graph, 200

def post_conllu_to_graph(body):  # noqa: E501
    """Get dependency analysis given a CoNLL-U format

    Get dependency analysis for a text by providing its already known CoNLL-U format # noqa: E501

    :param body: The conllu table corresponding to a text
    :type body: str

    :rvalue dep_graph: The dependency graph as an svg image (svg+xml format)
    :rtype: str
    """
    
    # Use convert_conllu_to_graph of the analysis module 
    try: 
        from tool.services import analysis
    except:
        logger.error("Unexpected error: "+str(sys.exc_info()))
        return "", 500
    else:
        logger.debug("Using analysis to return the result of conllu_to_graph")
        dep_graph = analysis.convert_conllu_to_graph(body)
        return dep_graph, 200


def post_text_to_conllu(body):  # noqa: E501
    """Get dependency analysis for a text, in CoNLL-U format

    Get dependency analysis for a text, in CoNLL-U format, by providing text and language # noqa: E501

    The following parameters are inside the function's parameter "body".

    :param text: 
    :type text: str
    :param lang: 
    :type lang: str
    :param comments: 
    :type comments: bool

    :rtype: str
    """
    
    text = body.get('text')
    lang = body.get('lang')
    if lang==None:
        lang = 'de' # default value for language
    comments = body.get('comments')
    if comments==None:
        comments = False # default value for comments

    # Use convert_text_to_conllu of the analysis module
    try: 
        from tool.services import analysis
    except:
        logger.error("Unexpected error: "+str(sys.exc_info()))
        return "", 500
    else:
        logger.debug("Using analysis to return the result of text_to_conllu")
        conllu = analysis.convert_text_to_conllu(text, lang, comments)
        return conllu, 200


def post_text_to_graph(body):  # noqa: E501
    """Get dependency analysis for a text, in CoNLL-U format

    Get dependency analysis for a text, as a dependency graph, by providing text and language # noqa: E501

    The following parameters are inside the function's parameter "body".

    :param text: 
    :type text: str
    :param lang: 
    :type lang: str
    :param comments: 
    :type comments: bool

    :rtype: str
    """

    text = body.get('text')
    lang = body.get('lang')
    if lang==None:
        lang = 'de' # default value for language
    comments = body.get('comments')
    if comments==None:
        comments = False # default value for comments
    
    # Use convert_text_to_graph of the analysis module    
    try: 
        from tool.services import analysis
    except:
        logger.error("Unexpected error: "+str(sys.exc_info()))
        return "", 500
    else:
        logger.debug("Using analysis to return the result of text_to_graph")
        dep_graph = analysis.convert_text_to_graph(text, lang)
        return dep_graph, 200
