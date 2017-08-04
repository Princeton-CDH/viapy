import logging
import time

from cached_property import cached_property
import requests
import rdflib
from rdflib.namespace import Namespace


logger = logging.getLogger(__name__)


SCHEMA_NS = Namespace('http://schema.org/')


class ViafAPI(object):
    """Wrapper for VIAF API.

    https://platform.worldcat.org/api-explorer/apis/VIAF
    """

    # NOTE: API urls use www prefix, but VIAF URIs do not

    #: base url for VIAF API methods
    api_base = "https://www.viaf.org/viaf"
    #: base url for VIAF URIs
    uri_base = "http://viaf.org/viaf"

    @classmethod
    def uri_from_id(cls, viaf_id):
        """Generate a canonical VIAF URI for the specified id"""
        return "%s/%s" % (cls.uri_base, viaf_id)

    def suggest(self, term):
        '''Query autosuggest API.  Returns a list of results, or an
        empty list if no suggestions are found or if something went wrong'''

        #  'viaf/AutoSuggest?query=[searchTerms]&callback[optionalCallbackName]
        autosuggest_url = '%s/AutoSuggest' % self.api_base
        response = requests.get(autosuggest_url,
                                params={'query': term},
                                headers={'accept': 'application/json'})
        logger.debug('autosuggest \'%s\': %s, %0.2f',
                     term, response.status_code, response.elapsed.total_seconds())

        if response.status_code == requests.codes.ok:
            return response.json().get('result', None) or []

        # if there was an http error, raise it
        response.raise_for_status()

        return []


class ViafEntity(object):
    '''Object for working with a single VIAF entity.

    :param viaf_id: viaf identifier (either integer or uri)
    '''
    def __init__(self, viaf_id):
        try:
            int(viaf_id)
            self.uri = ViafAPI.uri_from_id(viaf_id)
        except ValueError:
            # NOTE: do we need to canonicalize the URI in any way to
            # ensure RDF queries work properly?
            self.uri = viaf_id

    @property
    def uriref(self):
        '''VIAF URI reference as instance of :class:`rdflib.URIRef`'''
        return rdflib.URIRef(self.uri)

    @cached_property
    def rdf(self):
        '''VIAF data for this entity as :class:`rdflib.Graph`'''
        start = time.time()
        graph = rdflib.Graph()
        graph.parse(self.uri)
        logger.debug('Loaded VIAF RDF %s: %0.2f sec',
                     self.uri, time.time() - start)
        return graph

    # person-specific properties

    @property
    def birthdate(self):
        '''schema birthdate as :class:`rdflib.Literal`'''
        return self.rdf.value(self.uriref, SCHEMA_NS.birthDate)

    @property
    def deathdate(self):
        '''schema deathdate as :class:`rdflib.Literal`'''
        return self.rdf.value(self.uriref, SCHEMA_NS.deathDate)

    @property
    def birthyear(self):
        '''birth year'''
        if self.birthdate:
            return self.year_from_isodate(str(self.birthdate))

    @property
    def deathyear(self):
        '''death year'''
        if self.deathdate:
            return self.year_from_isodate(str(self.deathdate))

    # utility method for date parsing
    @classmethod
    def year_from_isodate(cls, date):
        '''Return just the year portion of an ISO8601 date.  Expects
        a string, returns an integer'''
        return int(date.split('-')[0])
