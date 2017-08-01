import os
from unittest.mock import patch

import requests
import rdflib

from viapy.api import ViafAPI, ViafEntity

FIXTURES_PATH = os.path.join(os.path.dirname(__file__), 'fixtures')


class TestViafAPI(object):

    def setUp(self):
        """Load the sample XML file and pass to the TestCase object"""
        fixture_file = os.path.join(FIXTURES_PATH, 'sample_viaf_rdf.xml')
        with open(fixture_file, 'r') as fixture:
            self.mock_rdf = fixture.read()

        graph = rdflib.Graph()
        self.empty_rdf = graph.serialize()

    def test_get_uri(self):
        assert ViafAPI.uri_from_id('1234') == \
            'http://viaf.org/viaf/1234'
        # numeric id should also work
        assert ViafAPI.uri_from_id(1234) == \
            'http://viaf.org/viaf/1234'

    @patch('viapy.api.requests')
    def test_suggest(self, mockrequests):
        viaf = ViafAPI()
        mockrequests.codes = requests.codes
        # Check that query with no matches still returns an empty list
        mock_result = {'query': 'notanauthor', 'result': None}
        mockrequests.get.return_value.status_code = requests.codes.ok
        mockrequests.get.return_value.json.return_value = mock_result
        assert viaf.suggest('notanauthor') == []
        mockrequests.get.assert_called_with(
            'https://www.viaf.org/viaf/AutoSuggest',
            headers={'accept': 'application/json'},
            params={'query': 'notanauthor'})

        # valid (abbreviated) response
        mock_result['result'] = [{
          "term": "Austen, Jane, 1775-1817",
          "displayForm": "Austen, Jane, 1775-1817",
          "recordID": "102333412"
        }]
        mockrequests.get.return_value.json.return_value = mock_result
        assert viaf.suggest('austen') == mock_result['result']

        # bad status code on the response - should still return an empty list
        mockrequests.get.return_value.status_code = requests.codes.forbidden
        assert viaf.suggest('test') == []


class TestViafEntity(object):

    test_id = 102333412
    test_uri = 'http://viaf.org/viaf/102333412'
    rdf_fixture = os.path.join(FIXTURES_PATH, '102333412_rdf.xml')

    def test_init(self):
        # numeric id (either int or string should work)
        ent = ViafEntity(self.test_id)
        assert ent.uri == self.test_uri
        ent = ViafEntity(str(self.test_id))
        assert ent.uri == self.test_uri
        # uri
        ent = ViafEntity(self.test_uri)
        assert ent.uri == self.test_uri

    def test_uriref(self):
        ent = ViafEntity(self.test_uri)
        assert ent.uriref == rdflib.URIRef(self.test_uri)

    @patch('viapy.api.rdflib')
    def test_rdf(self, mockrdflib):
        ent = ViafEntity(self.test_uri)
        assert ent.rdf == mockrdflib.Graph.return_value
        # should initialize a graph and parse uri data
        mockrdflib.Graph.assert_called_with()
        mockrdflib.Graph.return_value.parse.assert_called_with(
            self.test_uri)

    def test_properties(self):
        # use viaf id matching fixture rdf file
        ent = ViafEntity('89599270')

        test_rdf = rdflib.Graph()
        test_rdf.parse(self.rdf_fixture)

        with patch('viapy.api.rdflib.Graph') as mockgraph:
            mockgraph.return_value = test_rdf
            assert str(ent.birthdate) == '69'
            assert str(ent.deathdate) == '140'
            assert ent.birthyear == 69
            assert ent.deathyear == 140

    def test_year_from_isodate(self):
        assert ViafEntity.year_from_isodate('2001') == 2001
        assert ViafEntity.year_from_isodate('2002-01') == 2002
        assert ViafEntity.year_from_isodate('2004-03-05') == 2004



