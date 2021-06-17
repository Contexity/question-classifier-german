# coding: utf-8

# must run from the current folder

import conllu
import unittest
import sys
import os
from openapi_server.error_management.errors import BadRequestProblem
import pathlib
#abs_path = os.path.abspath(os.path.join('..', '..')) # add the path of the project's directory (openapi_server)
#print(abs_path)
#sys.path.insert(1, abs_path)

try: 
    from tool.services.analysis import *
except:
    print("Unexpected error:", sys.exc_info(), file=sys.stderr)

class TestAnalysis(unittest.TestCase):

    def test_check_line_endings_in_text(self):
        """ 
        Checks for errors when the text has different types of line endings.

        Checks if the function convert_text_to_conllu works for both types of inputs:
            - text with Windows-style line endings
            - text with Unix-style line endings
        """
        
        # Asign values to parameters for the function convert_text_to_conllu
        lang = 'de' # for both function calls
        # Load text1 (with Windows-style line endings)
        with open(pathlib.Path(__file__).parent.parent.joinpath('data','de','text_Win_line_endings.txt')) as f1:
            text1 = f1.read()
        # Load text2 (with Unix-style line endings)
        with open(pathlib.Path(__file__).parent.parent.joinpath('data','de','text_Unix_line_endings.txt')) as f2:
            text2 = f2.read()

        # Convert text1 and text2 to a CoNLL-U table each
        result1 = convert_text_to_conllu(text1, lang)
        result2 = convert_text_to_conllu(text2, lang)

        # Compare the two results. They must be equal.
        self.assertEqual(result1, result2, "The two CoNLL-U tables should be the same")

    @unittest.skip("not possible to test the outputs")
    def test_check_line_endings_in_conllu(self):
        """ 
        Checks for errors when the CoNLL-U string has different types of line endings.

        Checks if the function convert_conllu_to_graph works for both types of inputs:
            - CoNLL-U with Windows-style line endings
            - CoNLL-U with Unix-style line endings
        """
        
        # Asign values to body for the function convert_conllu_to_graph
        # Load conllu1 (with Windows-style line endings)
        with open(pathlib.Path(__file__).parent.parent.joinpath('data','de','conllu_Win_line_endings.txt')) as f:
            body1 = f.read()
        # Load conllu2 (with Unix-style line endings)
        with open(pathlib.Path(__file__).parent.parent.joinpath('data','de','conllu_Unix_line_endings.txt')) as f:
            body2 = f.read()

        # Convert conllu1 and conllu2 to a dependency graph each
        result1 = convert_conllu_to_graph(body1)
        result2 = convert_conllu_to_graph(body2)

        with open(pathlib.Path(__file__).parent.parent.joinpath('data','de','result_win.xml'), 'w') as f:
            f.write(result1)
        with open(pathlib.Path(__file__).parent.parent.joinpath('data','de','result_unix.xml'), 'w') as f:
            f.write(result2)

        # Compare the two results. They must be equal.
        self.assertEqual(result1, result2, "The two dependency graphs should be the same")

    def test_multiple_sentences(self):
        """ 
        Tests if the function convert_text_to_conllu works correctly with multiple sentences in the input text.
        """
        
        # Asign values to parameters for the function convert_text_to_conllu
        lang = 'de'
        with open(pathlib.Path(__file__).parent.parent.joinpath('data','de','text_Win_line_endings.txt')) as f:
            text = f.read()

        # Convert the text to a CoNLL-U table
        conllu_table = convert_text_to_conllu(text, lang)

        # Remove spaces at the beginning and the end of the table
        conllu_table = conllu_table.strip()

        # Break the table into smaller ones and save them in a list
        splitted_conllu_tables = conllu_table.split('\n\n')

        # Check the length of the list. It must be 2, because the input text contains two sentences.
        self.assertEqual(len(splitted_conllu_tables), 2, "Should be 2")

    def test_empty_text(self):
        """ 
        Check if the function convert_text_to_conllu works correctly when the text parameter is empty

        Check if the function convert_text_to_conllu raises a BadRequestProblem exception when the text parameter is empty
        """

        # Asign values to parameters for the function convert_text_to_conllu
        lang = 'de'
        text = ''
        
        # Check if the function convert_text_to_conllu raises a BadRequestProblem exception
        with self.assertRaises(BadRequestProblem):
            conllu_table = convert_text_to_conllu(text, lang)


    def test_empty_conllu_table(self):
        """ 
        Check if the function convert_conllu_to_graph works correctly when the body parameter is empty

        Check if the function convert_conllu_to_graph raises a BadRequestProblem exception when the body parameter is empty
        """

        # Asign value to body for the function convert_conllu_to_graph
        body = ''
        
        # Check if the function convert_conllu_to_graph raises a BadRequestProblem exception
        with self.assertRaises(BadRequestProblem):
            graph = convert_conllu_to_graph(body)

    def test_conllu_format(self):
        """ 
        Check if the function convert_conllu_to_graph works correctly when the body parameter has a wrong format

        Check if the function convert_conllu_to_graph raises a BadRequestProblem exception when the body parameter is not in the CoNLL-U format
        """

         # Asign a sentence to body instead of a CoNLL-U formatted string
        body = 'Not a conllu format'

        # Check if the function convert_conllu_to_graph raises a BadRequestProblem exception
        with self.assertRaises(BadRequestProblem):
            graph = convert_conllu_to_graph(body)

        
    def test_convert_text_to_conllu(self):
        """ 
        Checks if the function convert_text_to_conllu works correctly for an expected input
        """

        # Asign values to parameters for the function convert_text_to_conllu
        lang = 'de'
        with open(pathlib.Path(__file__).parent.parent.joinpath('data','de','text_Win_line_endings.txt')) as f:
            text = f.read()

        # Convert the text to a CoNLL-U table
        conllu_table = convert_text_to_conllu(text, lang)

        # Try to convert the conllu_table back to sentences with the help of the conllu module
        sentences = conllu.parse(conllu_table)

        # The above command should produce a list, unless there is a problem in the convert_text_to_conllu function, when it raises an exception
        self.assertEqual(type(sentences), list)

    def test_convert_text_to_graph(self):
        """ 
        Checks if the function convert_text_to_graph works correctly for an expected input
        """

        # Asign values to parameters for the function convert_text_to_graph
        lang = 'de'
        with open(pathlib.Path(__file__).parent.parent.joinpath('data','de','text_Win_line_endings.txt')) as f:
            text = f.read()

        # Convert the text to a dependency graph
        dep_graph = convert_text_to_graph(text, lang)

        # Check if the produced string starts with '<svg' which means that it's an svg-image
        self.assertEqual(dep_graph[:4], '<svg')

    def test_convert_conllu_to_graph(self):
        """ 
        Checks if the function convert_conllu_to_graph works correctly for an expected input
        """

        # Asign value to body for the function convert_conllu_to_graph
        with open(pathlib.Path(__file__).parent.parent.joinpath('data','de','conllu_Win_line_endings.txt')) as f:
            body = f.read()

        # Convert the CoNLL-U table to a dependency graph
        dep_graph = convert_conllu_to_graph(body)

        # Check if the produced string starts with '<svg' which means that it's an svg-image
        self.assertEqual(dep_graph[:4], '<svg')      

def run_tests():
    unittest.main()

if __name__=='__main__':
    unittest.main()