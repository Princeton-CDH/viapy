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
        print('kwargs')
        print(self.kwargs)
        print(self.args)
        # optionally filter by nametype if set
        if 'nametype' in self.kwargs:
            result = [item for item in result
                       if item['nametype'] == self.kwargs['nametype']]

        return JsonResponse({
            'results': [dict(
                id=viaf.uri_from_id(item['viafid']),
                text=item['displayForm'],
                nametype=item['nametype']
            # exclude any names that are not personal
            ) for item in result]
        })
