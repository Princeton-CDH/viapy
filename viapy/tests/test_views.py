import json
from unittest.mock import patch

from django.http import JsonResponse
from django.test import TestCase
from django.urls import reverse

from viapy.api import ViafAPI
from viapy.widgets import ViafWidget


class TestViafWidget(object):

    def test_render(self):
        widget = ViafWidget()
        # no value set - should not error
        rendered = widget.render('person', None, {'id': 123})
        assert '<p><br /><a id="viaf_uri" target="_blank" href=""></a></p>' \
            in rendered
        # test marked as "safe"?

        # uri value set - should be included in generated link
        uri = 'http://viaf.org/viaf/13103985/'
        rendered = widget.render('person', uri, {'id': 1234})
        assert '<a id="viaf_uri" target="_blank" href="%(uri)s">%(uri)s</a>' \
            % {'uri': uri} in rendered


class TestViews(TestCase):

    @patch('viapy.views.ViafAPI')
    def test_lookup(self, mockviafapi):
        # Sample of the dict passed by the api
        mock_response = [{
            'displayForm': 'Austen, Jane, 1775-1817',
            'term': 'Austen, Jane, 1775-1817',
            'viafid': '102333412',
            'nametype': 'personal',
        }]
        mockviafapi.return_value.suggest.return_value = mock_response
        # Get the actual URL from the API
        mockviafapi.return_value.uri_from_id = ViafAPI.uri_from_id

        lookup_url = reverse('viaf:lookup')
        result = self.client.get(lookup_url, {'q': 'austen'})
        assert result.status_code == 200
        # Pull the JSON response in and break it down
        assert isinstance(result, JsonResponse)
        data = json.loads(result.content.decode('utf-8'))
        # Should be a list with at least one dictionary, if actual result
        assert isinstance(data['results'], list)
        assert isinstance(data['results'][0], dict)
        # Now check for what needs to be in a dict to fill the autocomplete
        data = data['results'][0]
        assert data['id'] == 'http://viaf.org/viaf/102333412'
        assert data['text'] == 'Austen, Jane, 1775-1817'

    @patch('viapy.views.ViafAPI')
    def test_person_lookup(self, mockviafapi):
        person_lookup_url = reverse('viaf:person-lookup')
        print('url - %s' % person_lookup_url)
        # test that non-personal names are filtered out
        mock_response = [{
            "term": "Jersey",
            "displayForm": "Jersey",
            "nametype": "geographic",
            "lc": "n79086822",
            "dnb": "000438200",
            "selibr": "149410",
            "bne": "xx5289012",
            "viafid": "142485803",
            "score": "2567",
            "recordID": "142485803"
        }]
        mockviafapi.return_value.suggest.return_value = mock_response
        mockviafapi.return_value.uri_from_id = ViafAPI.uri_from_id
        result = self.client.get(person_lookup_url, {'q': 'jersey'})
        # should return an empty list because no personal names were returned
        data = json.loads(result.content.decode('utf-8'))
        assert not data['results']

