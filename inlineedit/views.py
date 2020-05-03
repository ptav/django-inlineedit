from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseServerError
from django.apps import apps
from django.db.models import Model as DjangoModel
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from typing import Callable

from .adaptors import get_adaptor_class


def handle_internal_errors(f: Callable) -> Callable:
    def decorator(*args, **kwargs) -> HttpResponse:
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(">>> Django-Inlineedit Error: {}".format(str(e)))
            return HttpResponseServerError(str(e), content_type="text/plain")
    return decorator


@handle_internal_errors
def inlineedit_form_submit(request: HttpRequest) -> JsonResponse:
    field_value = request.POST['field']
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

    adaptor_class = get_adaptor_class(adaptor)
    inline_adaptor = adaptor_class(db_object, field)

    inline_adaptor.save(field_value)
    if not inline_adaptor.has_edit_perm(request.user): raise PermissionDenied()

    value = inline_adaptor.display_value()
    empty_msg = "" if value else inline_adaptor.empty_message()

    out = {
        'value': value,
        'empty_message': empty_msg,
        'field_name': field_name,
        'adaptor': adaptor,
        'uuid': field_uuid
    }

    return JsonResponse(out)
