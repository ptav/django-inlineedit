import logging
from django import forms
from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseServerError
from django.apps import apps
from django.db.models import Model as DjangoModel
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from typing import Callable

from .adaptors import _get_adaptor_class_


logger = logging.getLogger(__name__)


def handle_internal_errors(f: Callable) -> Callable:
    def decorator(*args, **kwargs) -> HttpResponse:
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(str(e))
            return HttpResponseServerError(str(e), content_type="text/plain")
    return decorator


@handle_internal_errors
def inlineedit_form_submit(request: HttpRequest) -> JsonResponse:
    field_uuid = request.POST['uuid']

    try:
        # noinspection PyUnresolvedReferences
        session_data = request.session[field_uuid]
    except AttributeError:
        raise ImproperlyConfigured("The django application does not "
                                   "have the required session"
                                   "middleware enabled!")

    app_label, model_name, field_name, object_key, adaptor = tuple(session_data.split("."))
    model_class: DjangoModel = apps.get_model(app_label, model_name)

    db_object = model_class.objects.get(pk=object_key)
    field = db_object._meta.get_field(field_name)

    adaptor_class = _get_adaptor_class_(adaptor)
    inline_adaptor = adaptor_class(db_object, field, request.user)

    class _InlineeditForm(forms.Form):
        uuid = forms.fields.CharField(max_length=32, widget=forms.widgets.HiddenInput())
        field = inline_adaptor.form_field()

    form = _InlineeditForm(request.POST)
    if form.is_valid():
        field_value = form.cleaned_data['field']
        inline_adaptor.save(field_value)
        if not inline_adaptor.has_edit_perm(request.user): raise PermissionDenied()

        value = inline_adaptor.display_value()
        empty_msg = "" if value else inline_adaptor.empty_message()

        out = {
            'uuid': field_uuid,
            'value': value,
            'empty_message': empty_msg,
            'field_name': field_name,
            'adaptor': adaptor,
        }

        return JsonResponse(out)

    # if form is not valid
    raise ImproperlyConfigured("Form is not valid")

