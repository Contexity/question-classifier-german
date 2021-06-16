import os
import sys
abs_path = os.path.abspath(os.path.join('..', '..')) # add the path of the project's directory
sys.path.insert(1, abs_path)

from analysis import *


if __name__ == "__main__":

    # read arguments from command line
    parser = argparse.ArgumentParser()

    # Choose which function to call
    parser.add_argument("-ttc", "--convert_text_to_conllu", action="store_true", help="Convert a text to a CoNLL-U table. Takes arguments: 'text', 'lang'.")
    parser.add_argument("-ttg", "--convert_text_to_graph", action="store_true", help="Convert a text to a dependency graph. Takes arguments: 'text', 'lang'.")
    parser.add_argument("-ctg", "--convert_conllu_to_graph", action="store_true", help="Convert a CoNLL-U table to a dependency graph. Takes argument: 'conllu-table'.")

    # Arguments for the above functions (the user should choose the appropriate arguments for each function)
    parser.add_argument("--text", type=str, help="The text that will be subjected to dependency analysis")
    parser.add_argument("--lang", type=str, help="The language of the text")
    parser.add_argument("--conllu-table", type=str, help="The conllu table corresponding to a text")

    args = parser.parse_args()


    # RUN
    # load all the available language models in a dictionary
    print("Loading models...")
    nlp_models = load_nlp_models()

    if args.convert_text_to_conllu:
        print(convert_text_to_conllu(args.text, args.lang, nlp_models))
    elif args.convert_text_to_graph:
        print(convert_text_to_graph(args.text, args.lang, nlp_models))
    elif args.convert_conllu_to_graph:
        print(convert_conllu_to_graph(args.conllu-table))
    else:
        print("Error. You haven't selected a function, please select one of the three functions provided.")
