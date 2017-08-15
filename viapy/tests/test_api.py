import json
import os
from unittest.mock import patch

import requests
import rdflib

from viapy.api import ViafAPI, ViafEntity, SRUResult, SRUItem

FIXTURES_PATH = os.path.join(os.path.dirname(__file__), 'fixtures')


class TestViafAPI(object):

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


    @patch('viapy.api.requests')
    def test_search(self, mockrequests):
        viaf = ViafAPI()
        mockrequests.codes = requests.codes

        sru_fixture = os.path.join(FIXTURES_PATH, 'sru_search.json')
        with open(sru_fixture) as srufile:
            mock_result = json.load(srufile)
        mockrequests.get.return_value.status_code = requests.codes.ok
        mockrequests.get.return_value.json.return_value = mock_result
        results = viaf.search('stephen benet')
        assert isinstance(results, list)
        assert isinstance(results[0], SRUItem)
        mockrequests.get.assert_called_with(
            'https://www.viaf.org/viaf/search',
            # headers={'accept': 'application/json'},
            params={'query': 'stephen benet', 'httpAccept': 'application/json',
                    'maximumRecords': 50})

        # sample empty result
        mockrequests.get.return_value.json.return_value = {
            'searchRetrieveResponse': {
                'version': "1.1",
                'numberOfRecords': "0",
                'resultSetIdleTime': "1"
            }
        }
        results = viaf.search('stephen benet')
        assert not results

    def test_find_person(self):
        viaf = ViafAPI()
        term = 'stephen benet'
        with patch.object(viaf, 'search') as mocksearch:
            viaf.find_person(term)

        mocksearch.assert_called_with('local.personalNames all "%s"' % term)

    def test_find_corporate(self):
        viaf = ViafAPI()
        term = 'library of congress'
        with patch.object(viaf, 'search') as mocksearch:
            viaf.find_corporate(term)

        mocksearch.assert_called_with('local.corporateNames all "%s"' % term)

    def test_find_place(self):
        viaf = ViafAPI()
        term = 'princeton'
        with patch.object(viaf, 'search') as mocksearch:
            viaf.find_place(term)

        mocksearch.assert_called_with('local.geographicNames all "%s"' % term)


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
        # load fixture
        test_rdf = rdflib.Graph()
        test_rdf.parse(self.rdf_fixture)

        # patch fixture in to ViafEntity rdf property
        with patch.object(ViafEntity, 'rdf', new=test_rdf):
            assert str(ent.birthdate) == '69'
            assert str(ent.deathdate) == '140'
            assert ent.birthyear == 69
            assert ent.deathyear == 140

    def test_year_from_isodate(self):
        assert ViafEntity.year_from_isodate('2001') == 2001
        assert ViafEntity.year_from_isodate('2002-01') == 2002
        assert ViafEntity.year_from_isodate('2004-03-05') == 2004


def test_sru_result():
    # test SRUResult class properties
    sru_fixture = os.path.join(FIXTURES_PATH, 'sru_search.json')
    with open(sru_fixture) as srufile:
        sru_data = json.load(srufile)
    sru_res = SRUResult(sru_data)
    assert sru_res.total_results == 13
    assert isinstance(sru_res.records, list)
    assert isinstance(sru_res.records[0], SRUItem)
    assert len(sru_res.records) == 5


def test_sru_item():
    # test SRUItem class
    sru_fixture = os.path.join(FIXTURES_PATH, 'sru_search.json')
    with open(sru_fixture) as srufile:
        sru_data = json.load(srufile)
    sru_item = SRUResult(sru_data).records[0]
    assert sru_item.uri == "http://viaf.org/viaf/888145424579886830405/"
    assert sru_item.viaf_id == "888145424579886830405"
    assert sru_item.nametype == "UniformTitleExpression"
    assert sru_item.label == "Benét, Stephen Vincent, 1898-1943. | John Brown's Body | Russian 1979"

    # label when data is a list
    sru_item.recordData.mainHeadings.data = [
        sru_item.recordData.mainHeadings.data
    ]
    assert sru_item.label == "Benét, Stephen Vincent, 1898-1943. | John Brown's Body | Russian 1979"