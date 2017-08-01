from dal import autocomplete
from django.utils.safestring import mark_safe


class ViafWidget(autocomplete.Select2):
    '''Custom autocomplete select widget that displays VIAF id as a link.
    Extends :class:`dal.autocomplete.Select2`.'''

    def render(self, name, value, attrs=None):
        widget = super(ViafWidget, self).render(name, value, attrs)
        return mark_safe(
            '%s<p><br /><a id="viaf_uri" target="_blank" href="%s">%s</a></p>' % \
            (widget, value or '', value or ''))
