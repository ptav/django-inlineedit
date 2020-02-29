from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseServerError
from django.apps import apps
from django.db.models import Model as DjangoModel
from django.core.exceptions import ImproperlyConfigured
from typing import Callable

from .adaptors.selector import get_adaptor_class


def handle_internal_errors(f: Callable) -> Callable:
    def decorator(*args, **kwargs) -> HttpResponse:
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return HttpResponseServerError(str(e), content_type="text/plain")
    return decorator


@handle_internal_errors
def inlineedit_form_submit(request: HttpRequest) -> JsonResponse:
    field_value: str = request.POST['field']
    field_uuid: str = request.POST['id']

    try:
        # noinspection PyUnresolvedReferences
        session_data: str = request.session[field_uuid]
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

    inline_adaptor.field_value = field_value

    out = {
        'field_name': field_name,
        'value': field_value,
        'display_type': inline_adaptor.DISPLAY_TYPE,
        'adaptor': inline_adaptor.ADAPTOR_NAME,
        'uuid': field_uuid
    }

    return JsonResponse(out)
