import logging
from typing import Union, Optional
from django.db.models import Model as DjangoModel, Field as DjangoField
from django.contrib.auth.models import User, AnonymousUser
from django.utils.html import format_html
from django.conf import settings

from ..access import __check_edit_access__


logger = logging.getLogger(__name__)


if 'reversion' in settings.INSTALLED_APPS:
    import reversion
    _reversion_installed = True
    logger.info("django-reversion is enabled in django-Inlineedit")
else:
    _reversion_installed = False
    logger.info("django-reversion is disabled in django-Inlineedit")


class BasicAdaptor:
    "Simplest adaptor and interface"
    
    def __init__(
            self,
            model_object: DjangoModel,
            field: DjangoField,
            user: Optional[Union[User, AnonymousUser]] = None,
            *args,
            **kwargs
    ):
        self._model: DjangoModel = model_object
        self._app = model_object._meta.app_label
        self._field = field
        self._user = user
        
        if _reversion_installed:
            self._reversion_enabled = True
        else:
            self._reversion_enabled = False

    def form_field(self):
        "Return the DjangoFormField object"
        return self._field.formfield()

    def empty_message(self):
        "Returns message to show users if field is empty. The default is 'Hover here to edit <name>'"
        return "Hover here to edit {}".format(self._field.verbose_name)

    def db_value(self):
        "Returns the field value as stored in the db"
        return getattr(self._model, self._field.attname)        

    def display_value(self):
        "Returns the field value to be shown to users"
        
        "_value_type is used to force type back to the correct type"
        db = self.db_value()
        
        if self._field.choices: # convert to external representation
            display = dict(self._field.choices).get(db,"--")
        elif db == None:
            display = "N/A"
        elif isinstance(db, bool):
            display = format_html("&check;" if db else "&cross;")
        else:
            display = db
        
        return display

    def save(self, value):
        "Save a new field value to the db. The default version supports django-reversions if that is enabled"
        setattr(self._model, self._field.attname, value)
        if self._reversion_enabled:
            with reversion.create_revision():
                self._model.save()
                if self._user:
                    reversion.set_user(self._user)
        else:
            self._model.save()

    def has_edit_perm(self, user):
        return __check_edit_access__(user, self._model, self._field)

