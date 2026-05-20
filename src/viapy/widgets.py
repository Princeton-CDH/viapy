from dal import autocomplete
from django.utils.safestring import mark_safe


class ViafWidget(autocomplete.Select2):
    """Custom autocomplete select widget that displays VIAF id as a link.
    Extends :class:`dal.autocomplete.Select2`."""

    def render(self, name, value, renderer=None, attrs=None):
        # select2 filters based on existing choices (non-existent here),
        # so when a value is set, add it to the list of choices
        if value:
            self.choices = [(value, value)]
        widget = super().render(name, value, attrs)
        return mark_safe(
            f'{widget}<p><br /><a id="viaf_uri" target="_blank" href="{value or ""}">{value or ""}</a></p>'
        )
