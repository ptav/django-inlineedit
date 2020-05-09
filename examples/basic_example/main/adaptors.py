from django import forms

from inlineedit.adaptors import BasicAdaptor


"Custom adaptor examples"


class MillionsAdaptor(BasicAdaptor):
    "Basic custom adaptor example"

    def display_value(self):
        return f"£{self.db_value()} millions"


class BlockedAdaptor(BasicAdaptor):
    "Demonstrate adaptor level permission setting"
    def has_edit_perm(self, user):
        return False


class DatePicker(BasicAdaptor):
    "Integrate with Bootstrap date picker"

    def form_field(self):
        "Return the DjangoFormField object"
        f = self._field.formfield()
        f.widget = forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date', 'class': 'form-control'})
        return f