from django.utils.translation import gettext_lazy as _
from django.contrib.admin.views.autocomplete import AutocompleteJsonView

class CustomAutocompleteJsonView(AutocompleteJsonView):
    def serialize_result(self, obj, to_field_name):
        text = str(obj.select2() if hasattr(obj, 'select2') else obj)
        return {'id': str(getattr(obj, to_field_name)), 'text': text}  

def autocomplete_view(self, request):
    return CustomAutocompleteJsonView.as_view(admin_site=self)(request)
