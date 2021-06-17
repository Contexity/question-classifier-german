# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_get_conllu_to_graph(self):
        """Test case for get_conllu_to_graph

        Get dependency analysis given a CoNLL-U format
        """
        query_string = [('conllu', 'conllu_example')]
        headers = { 
            'Accept': 'image/svg+xml',
        }
        response = self.client.open(
            '/dependency-graph-from-conllu',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_text_to_conllu(self):
        """Test case for get_text_to_conllu

        Get dependency analysis for a text, in CoNLL-U format
        """
        query_string = [('text', This is a test for English text.),
                        ('lang', 'de'),
                        ('comments', False)]
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

    def test_get_text_to_graph(self):
        """Test case for get_text_to_graph

        Get dependency analysis for a text
        """
        query_string = [('text', This is a test for English text.),
                        ('lang', 'de')]
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

    @unittest.skip("text/plain; charset&#x3D;utf-8 not supported by Connexion")
    def test_post_conllu_to_graph(self):
        """Test case for post_conllu_to_graph

        Get dependency analysis given a CoNLL-U format
        """
        body = 'body_example'
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

    @unittest.skip("multipart/form-data not supported by Connexion")
    def test_post_text_to_conllu(self):
        """Test case for post_text_to_conllu

        Get dependency analysis for a text, in CoNLL-U format
        """
        headers = { 
            'Accept': 'text/plain',
            'Content-Type': 'multipart/form-data',
        }
        data = dict(text='text_example',
                    lang='de',
                    comments=False)
        response = self.client.open(
            '/conllu-from-text',
            method='POST',
            headers=headers,
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("multipart/form-data not supported by Connexion")
    def test_post_text_to_graph(self):
        """Test case for post_text_to_graph

        Get dependency analysis for a text, in CoNLL-U format
        """
        headers = { 
            'Accept': 'text/plain',
            'Content-Type': 'multipart/form-data',
        }
        data = dict(text='text_example',
                    lang='de',
                    comments=False)
        response = self.client.open(
            '/dependency-graph-from-text',
            method='POST',
            headers=headers,
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
