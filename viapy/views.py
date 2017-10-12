from django.http import JsonResponse
from dal import autocomplete

from viapy.api import ViafAPI


class ViafLookup(autocomplete.Select2ListView):
    '''View to provide VIAF suggestions for autocomplete lookup.
    Based on :class:`dal.autocompleteSelect2ListView`.  Expects search
    term as query string parameter `q`. Returns viaf URI as identifier
    and display form as text.
    '''

    def get(self, request, *args, **kwargs):
        """Return JSON with suggested VIAF ids and display names."""
        viaf = ViafAPI()
        result = viaf.suggest(self.q)

        # optionally filter by nametype if set
        if 'nametype' in self.kwargs:
            result = [item for item in result
                       if item['nametype'] == self.kwargs['nametype']]

        return JsonResponse({
            'results': [dict(
                id=viaf.uri_from_id(item['viafid']),
                id_number=item['viafid'],
                text=item['displayForm'],
                nametype=item['nametype']
            # exclude any names that are not personal
            ) for item in result]
        })


class ViafSearch(autocomplete.Select2ListView):
    '''View to provide VIAF suggestions for autocomplete lookup.
    Based on :class:`dal.autocompleteSelect2ListView`.  Expects search
    term as query string parameter `q`. Returns viaf URI as identifier
    and display form as text.
    '''

    def get(self, request, *args, **kwargs):
        """Return JSON with suggested VIAF ids and display names."""
        viaf = ViafAPI()

        # search for specific kind of name if set
        nametype = self.kwargs.get('nametype', None)
        if nametype == 'personal':
            result = viaf.find_person(self.q)
        else:
            result = viaf.search(self.q)

        # check for empty search result and return empty json response
        if result is None:
            return JsonResponse({'results': []})

        return JsonResponse({
            'results': [dict(
                # id=viaf.uri_from_id(item.recordData.viafID),
                id=item.uri,
                id_number=item.viaf_id,
                text=item.label,
                nametype=item.nametype,
                # possibly useful to include, since we have them (for people)
                birth=item.recordData.birthDate,
                death=item.recordData.deathDate,
            # exclude any names that are not personal
            ) for item in result]
        })
