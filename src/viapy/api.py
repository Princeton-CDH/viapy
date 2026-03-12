import logging
import re
import time

from attrdict import AttrMap
from cached_property import cached_property
import requests
import rdflib
from rdflib.namespace import Namespace


logger = logging.getLogger(__name__)


SCHEMA_NS = Namespace("http://schema.org/")


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
        """Query autosuggest API.  Returns a list of results, or an
        empty list if no suggestions are found or if something went wrong"""

        #  'viaf/AutoSuggest?query=[searchTerms]&callback[optionalCallbackName]
        autosuggest_url = "%s/AutoSuggest" % self.api_base
        response = requests.get(
            autosuggest_url,
            params={"query": term},
            headers={"accept": "application/json"},
        )
        logger.debug(
            "autosuggest '%s': %s %s, %0.2f",
            term,
            response.status_code,
            response.reason,
            response.elapsed.total_seconds(),
        )

        if response.status_code == requests.codes.ok:
            return response.json().get("result", None) or []

        # if there was an http error, raise it
        response.raise_for_status()

        return []

    def search(self, query):
        """Query VIAF seach interface.  Returns a list of :class:`SRUItem`
        :param query: CQL query in viaf syntax (e.g., ``cql.any all "term"``)
        """
        search_url = "%s/search" % self.api_base
        params = {
            "query": query,
            "maximumRecords": 10,  # TODO: configurable ?
            # sort by number of holdings (default sort on web search)
            # - so better known names show up first
            "sortKey": "holdingscount",
        }

        response = requests.get(search_url, params=params, headers={"Accept": "application/json"})
        logger.debug(
            "search '%s': %s %s, %0.2f",
            params["query"],
            response.status_code,
            response.reason,
            response.elapsed.total_seconds(),
        )
        if response.status_code == requests.codes.ok:
            data = SRUResult(response.json())
            if data.total_results:
                return data.records

        # if response was not ok, raise the error
        response.raise_for_status()

    def _find_type(self, fltr, value):
        return self.search('%s all "%s"' % (fltr, value))

    def find_person(self, name):
        """Search VIAF for local.personalNames"""
        return self._find_type("local.personalNames", name)

    def find_corporate(self, name):
        """Search VIAF for local.corporateNames"""
        return self._find_type("local.corporateNames", name)

    def find_place(self, name):
        """Search VIAF for local.geographicNames"""
        return self._find_type("local.geographicNames", name)


class ViafEntity(object):
    """Object for working with a single VIAF entity.

    :param viaf_id: viaf identifier (either integer or uri)
    """

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
        """VIAF URI reference as instance of :class:`rdflib.URIRef`"""
        return rdflib.URIRef(self.uri)

    @cached_property
    def rdf(self):
        """VIAF data for this entity as :class:`rdflib.Graph`"""
        start = time.time()
        graph = rdflib.Graph()
        # 2025 update: Accept header now required, so use requests.get to retrieve RDF
        response = requests.get(self.uri, headers={"Accept": "application/rdf+xml"})
        response.raise_for_status()  # raise HTTPError on non-success status
        graph.parse(data=response.text, format="xml")
        logger.debug("Loaded VIAF RDF %s: %0.2f sec", self.uri, time.time() - start)
        return graph

    # person-specific properties

    @property
    def birthdate(self):
        """schema birthdate as :class:`rdflib.Literal`"""
        return self.rdf.value(self.uriref, SCHEMA_NS.birthDate)

    @property
    def deathdate(self):
        """schema deathdate as :class:`rdflib.Literal`"""
        return self.rdf.value(self.uriref, SCHEMA_NS.deathDate)

    @property
    def birthyear(self):
        """birth year"""
        if self.birthdate:
            return self.year_from_isodate(str(self.birthdate))

    @property
    def deathyear(self):
        """death year"""
        if self.deathdate:
            return self.year_from_isodate(str(self.deathdate))

    # utility method for date parsing
    @classmethod
    def year_from_isodate(cls, date):
        """Return just the year portion of an ISO8601 date.  Expects
        a string, returns an integer. Supports negative dates."""
        negative = False
        # if the date starts with a dash, strip off before trying to split
        if date.startswith("-"):
            date = date[1:]
            negative = True
        value = int(date.split("-")[0])
        if negative:
            return -value
        return value


class SRUResult(object):
    """SRU search result object, for use with :meth:`ViafAPI.search`."""

    def __init__(self, data):
        self._data = data.get("searchRetrieveResponse", {})

    @cached_property
    def total_results(self):
        """number of records matching the query"""
        return int(self._data.get("numberOfRecords", {}).get("content", 0))

    @cached_property
    def records(self):
        """List of results as :class:`SRUItem`."""
        record_or_records = self._data.get("records", {}).get("record")
        if isinstance(record_or_records, dict):
            return [SRUItem(self.normalize_record(record_or_records))]
        elif isinstance(record_or_records, list):
            return [SRUItem(self.normalize_record(d)) for d in record_or_records]
        return []

    def normalize_record(self, data):
        """Added in May 2025 to match updates to the /search API records, where
        the JSON response now uses namespaced keys that increase per result:
        ns2, ns3, ns4, and so on, applying to most subkeys (ns2:VIAFCluster,
        ns2:Document, etc). This method strips all nsX: prefixes recursively"""
        if isinstance(data, dict):
            return {
                re.sub(r"^ns\d+:", "", key): self.normalize_record(value)
                for key, value in data.items()
            }
        elif isinstance(data, list):
            return [self.normalize_record(item) for item in data]
        else:
            return data

class SRUItem(AttrMap):
    """Single item returned by a SRU search, for use with
    :meth:`ViafAPI.search` and :class:`SRUResult`.
    
    The `VIAFCluster` attribute was added to each property lookup in 2025 to
    match updates to the /search API's JSON response."""

    @property
    def uri(self):
        """VIAF URI for this result"""
        return self.recordData.VIAFCluster.Document["about"]

    @property
    def viaf_id(self):
        """VIAF numeric identifier"""
        return self.recordData.VIAFCluster.viafID

    @property
    def nametype(self):
        """type of name (personal, corporate, title, etc)"""
        return self.recordData.VIAFCluster.nameType

    @property
    def label(self):
        """first main heading for this item"""
        try:
            return self.recordData.VIAFCluster.mainHeadings.data[0].text
        except (KeyError, IndexError):
            return self.recordData.VIAFCluster.mainHeadings.data.text
