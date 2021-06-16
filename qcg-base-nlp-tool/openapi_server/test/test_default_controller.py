# coding: utf-8

from __future__ import absolute_import
import unittest
import os
import sys
abs_path = os.path.abspath(os.path.join('..','..'))
sys.path.insert(1, abs_path)

from flask import json
from six import BytesIO

from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    #@unittest.skip("text/plain; charset&#x3D;utf-8 not supported by Connexion")
    def test_conllu_to_graph(self):
        """Test case for conllu_to_graph

        Get dependency analysis given a CoNLL-U format
        """
        body = "1 meine  meinen  DET  PPOSAT  _  2  nk  _  _2  karte  karte  NOUN  NN  _  3  sb  _  _3  ist  sein  AUX  VAFIN  _  0  root  _  _4  verloren  verlieren  VERB  VVPP  _  3  pd  _  SpaceAfter=No"
        headers = { 
            'Accept': 'image/svg+xml',
            'Content-Type': 'text/plain; charset&#x3D;utf-8',
        }
        response = self.client.open(
            '/dependency-graph-from-conllu',
            method='POST',
            headers=headers,
            data=json.dumps(body),
            content_type='text/plain; charset=utf-8')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_text_to_conllu(self):
        """Test case for text_to_conllu

        Get dependency analysis for a text, in CoNLL-U format
        """
        query_string = [('text', "This is a test for English text."),
                        ('lang', 'en')]
        headers = { 
            'Accept': 'text/plain',
        }
        response = self.client.open(
            '/conllu-from-text',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_text_to_graph(self):
        """Test case for text_to_graph

        Get dependency analysis for a text
        """
        query_string = [('text', "This is a test for English text."),
                        ('lang', 'en')]
        headers = { 
            'Accept': 'image/svg+xml',
        }
        response = self.client.open(
            '/dependency-graph-from-text',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
