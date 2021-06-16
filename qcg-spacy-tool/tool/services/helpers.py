''' This module contains helper functions for the analysis. '''

import json
from collections import OrderedDict

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

    # import nlp models (they first need to be downloaded from spacy using, e.g.: 
    # python -m spacy download en_core_web_sm)
    import de_core_news_md
    import en_core_web_md

    # Initialize dictionary
    nlp_models = {}

    # Load and store language models
    nlp_models['de'] = de_core_news_md.load()
    nlp_models['en'] = en_core_web_md.load()

    return nlp_models

def remove_comments_in_conllu(conllu_table):
    """ Removes comment lines from a CoNLL-U-formatted table

    :param conllu_table: The CoNLL-U table as a string
    :type conllu_table: str

    :rvalue conllu_output_table: The CoNLL-U table, without comment-lines, as a string
    :rtype conllu_output_table: str

    :Example: Example of a CoNLL-U table with a comment in its first line
    *Input table*
    # sent_id 1
    "1	This	this	DET	DT	_	2	nsubj	_	_
    2	is	be	AUX	VBZ	_	0	root	_	_
    3	a	a	DET	DT	_	4	det	_	_
    4	sentence	sentence	NOUN	NN	_	2	attr	_	SpaceAfter=No
    5	.	.	PUNCT	.	_	2	punct	_	_"

    *Output table*
    "1	This	this	DET	DT	_	2	nsubj	_	_
    2	is	be	AUX	VBZ	_	0	root	_	_
    3	a	a	DET	DT	_	4	det	_	_
    4	sentence	sentence	NOUN	NN	_	2	attr	_	SpaceAfter=No
    5	.	.	PUNCT	.	_	2	punct	_	_"
    """

    conllu_output_table = ""
    conllu_list = conllu_table.split("\n")
    # Adds to the final conllu table only the lines that don't start with '#' (no comment-lines)
    for sentence in conllu_list:
        if not(sentence.startswith('#')):
            conllu_output_table += sentence + "\n"

    return conllu_output_table

def split_conllu_into_sentences(conllu_table):
    """ Splits the CoNLL-U table in smaller ones
    
    Splits the CoNLL-U table corresponding to the whole text in smaller tables; one for each sentence

    :param conllu_table: The CoNLL-U table as a string
    :type conllu_table: str

    :rvalue splitted_conllu_tables: List with the CoNLL-U tables for each sentence
    :rtype splitted_conllu_tables: list

    :Example: Example of a CoNLL-U table that consists of two smaller ones
    *Input string*
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

    *Output list*
    ["# sent_id 1
    1	This	this	DET	DT	_	2	nsubj	_	_
    2	is	be	AUX	VBZ	_	0	root	_	_
    3	a	a	DET	DT	_	4	det	_	_
    4	sentence	sentence	NOUN	NN	_	2	attr	_	SpaceAfter=No
    5	.	.	PUNCT	.	_	2	punct	_	_",
    "# sent_id 2
    1	This	this	DET	DT	_	2	nsubj	_	_
    2	is	be	AUX	VBZ	_	0	root	_	_
    3	another	another	DET	DT	_	4	det	_	_
    4	sentence	sentence	NOUN	NN	_	2	attr	_	SpaceAfter=No
    5	.	.	PUNCT	.	_	2	punct	_	SpaceAfter=No"]
    """
    # Remove spaces at the beginning and end of the table
    conllu_table = conllu_table.strip()

    # Break the table into smaller ones and save them in a list
    splitted_conllu_tables = conllu_table.split('\n\n')

    return splitted_conllu_tables

def concat_displacy_dicts(displacy_dicts_list):
    """ Concatenates multiple displacy dicts into a single one

    Concatenate displacy dicts, in order that the indices of the words in each dictionary don't
    start from 0 but from the integer that follows the last index of the dictionary of the 
    sentence preceding the current sentence.

    :param displacy_dicts_list: List with the dictionaries that contain DisplaCy's format for each sentence
    :type displacy_dicts_list: list

    :rvalue whole_displacy_dict: The output dictionary that is a merge of the input list
    :rtype whole_displacy_dict: dict

    :Example:
    *List with two input dictionaries*
    [
        {
        "words": [
            {"text": "This", "tag": "DET"},
            {"text": "is", "tag": "AUX"},
            {"text": "a", "tag": "DET"},
            {"text": "sentence", "tag": "NOUN"}
            {"text": ".", "tag": "PUNCT"}
        ],
        "arcs": [
            {"start": 0, "end": 1, "label": "nsubj", "dir": "left"},
            {"start": 2, "end": 3, "label": "det", "dir": "left"},
            {"start": 1, "end": 3, "label": "attr", "dir": "right"}
            {"start": 1, "end": 4, "label": "punct", "dir": "right"}
        ]
        },

        {
        "words": [
            {"text": "This", "tag": "DET"},
            {"text": "is", "tag": "AUX"},
            {"text": "another", "tag": "DET"},
            {"text": "sentence", "tag": "NOUN"}
            {"text": ".", "tag": "PUNCT"}
        ],
        "arcs": [
            {"start": 0, "end": 1, "label": "nsubj", "dir": "left"},
            {"start": 2, "end": 3, "label": "det", "dir": "left"},
            {"start": 1, "end": 3, "label": "attr", "dir": "right"}
            {"start": 1, "end": 4, "label": "punct", "dir": "right"}
        ]
        }
    ]

    *Output dictionary*
    {
    "words": [
        {"text": "This", "tag": "DET"},
        {"text": "is", "tag": "AUX"},
        {"text": "a", "tag": "DET"},
        {"text": "sentence", "tag": "NOUN"}
        {"text": ".", "tag": "PUNCT"},
        {"text": "This", "tag": "DET"},
        {"text": "is", "tag": "AUX"},
        {"text": "another", "tag": "DET"},
        {"text": "sentence", "tag": "NOUN"}
        {"text": ".", "tag": "PUNCT"}
    ],
    "arcs": [
        {"start": 0, "end": 1, "label": "nsubj", "dir": "left"},
        {"start": 2, "end": 3, "label": "det", "dir": "left"},
        {"start": 1, "end": 3, "label": "attr", "dir": "right"}
        {"start": 1, "end": 4, "label": "punct", "dir": "right"},
        {"start": 5, "end": 6, "label": "nsubj", "dir": "left"},
        {"start": 7, "end": 8, "label": "det", "dir": "left"},
        {"start": 6, "end": 8, "label": "attr", "dir": "right"}
        {"start": 6, "end": 9, "label": "punct", "dir": "right"}
    ]
    }
    """
    num_previous_words = 0
    for id, displacy_dict in enumerate(displacy_dicts_list):
        if id>0:
            num_previous_words += len(displacy_dicts_list[id-1]["words"])
            for arc in displacy_dict["arcs"]:
                arc["start"] += num_previous_words
                arc["end"] += num_previous_words

            whole_displacy_dict["words"] += displacy_dict["words"]
            whole_displacy_dict["arcs"] += displacy_dict["arcs"]
        else:
            whole_displacy_dict = displacy_dict
    
    return whole_displacy_dict

########################### 
#Source https://github.com/explosion/spaCy/issues/1215
def conll_u_string2displacy_json(conll_u_sent_string): 
    """
    Converts a single CONLL-U formatted sentence to the displaCy json format.
    CONLL-U specification: http://universaldependencies.org/format.html
    """   
    
    conll_u_lines = [line for line in conll_u_sent_string.split("\n") \
                     if line[0].isnumeric()]

    displacy_json = {"arcs": [], "words": []}
    for tabbed_line in conll_u_lines:
        word_line = OrderedDict()
        word_line["id"], word_line["form"], word_line["lemma"], \
        word_line["upostag"], word_line["xpostag"], word_line["feats"], \
        word_line["head"], word_line["deprel"], word_line["deps"], \
        word_line["misc"] = tabbed_line.split("\t")

        word_line["id"] = convert2zero_based_numbering(word_line["id"])
        if word_line["head"] != "_":
            word_line["head"] = convert2zero_based_numbering(word_line["head"])       
        
        if word_line["deprel"] != "root" and word_line["head"] != "_":
            word_line = get_start_and_end(word_line)
            word_line = set_arrow_direction(word_line)
            displacy_json["arcs"].append({"dir": word_line["dir"],
                                          "end": word_line["end"],
                                          "label": word_line["deprel"],
                                          "start": word_line["start"]})
            
        displacy_json["words"].append({"tag": word_line["upostag"],
                                       "text": word_line["form"]})

    displacy_json = (json.dumps(displacy_json, indent=4))
    return displacy_json

def set_arrow_direction(word_line):
    """
    Sets the orientation of the arrow that notes the directon of the dependency
    between the two units.
    """

    if int(word_line["id"]) > int(word_line["head"]):
        word_line["dir"] = "right"
    elif int(word_line["id"]) < int(word_line["head"]):
        word_line["dir"] = "left"
    return word_line

def convert2zero_based_numbering(word_line_field):
    "CONLL-U numbering starts at 1, displaCy's at 0..."

    word_line_field = str(int(word_line_field) - 1)
    return word_line_field

def get_start_and_end(word_line):
    """
    Displacy's 'start' value is the lowest value amongst the ID and HEAD values,
    and the 'end' is always the highest. 'Start' and 'End' have nothing to do
    with dependency which is indicated by the arrow direction, not the line
    direction.
    """

    word_line["start"] = min([int(word_line["id"]), int(word_line["head"])])
    word_line["end"] = max([int(word_line["id"]), int(word_line["head"])])
    return word_line
###########################