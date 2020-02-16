from django.db.models import Model as DjangoModel, Field as DjangoField
from django.forms import Field as DjangoFormField
from django.contrib.auth.models import User, AnonymousUser
from typing import Union, Optional
try:
    import reversion
    _reversion_installed = True
except ImportError:
    _reversion_installed = False


class InlineFieldAdaptor:
    def __init__(
            self,
            model_object: DjangoModel,
            field: DjangoField,
            user_object: Optional[Union[User, AnonymousUser]] = None
    ):
        self._model: DjangoModel = model_object
        self._field = field
        self._user = user_object

        if _reversion_installed:
            self._reversion_enabled = True
        else:
            self._reversion_enabled = False

    @property
    def form_field(self) -> DjangoFormField:
        return self._field.formfield()

    @property
    def field_value(self) -> str:
        db_value = getattr(self._model, self._field.attname)
        if self._field.choices:
            value_display_mapping = dict(self._field.choices)
            return value_display_mapping.get(db_value)
        elif not db_value:
            return '<span style="opacity:0.5;">Hover to add {}</span>'.format(self._field.attname)
        return db_value

    @field_value.setter
    def field_value(self, value: str):
        setattr(self._model, self._field.attname, value)
        if self._reversion_enabled:
            with reversion.create_revision():
                self._model.save()
                if self._user:
                    reversion.set_user(self._user)
        else:
            self._model.save()
