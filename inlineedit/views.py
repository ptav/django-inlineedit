from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseServerError
from django.apps import apps
from django.db.models import Model as DjangoModel
from inlineedit.adaptors.basic import InlineFieldAdaptor
from inlineedit.adaptors.ckeditor import CKEditorFieldAdaptor
from django.core.exceptions import ImproperlyConfigured
from typing import Callable


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

    if adaptor == "basic":
        # noinspection PyProtectedMember
        inline_adaptor = InlineFieldAdaptor(
            model_object=db_object,
            field=db_object._meta.get_field(field_name)
        )
    elif adaptor == "ckeditor":
        # noinspection PyProtectedMember
        inline_adaptor = CKEditorFieldAdaptor(
            model_object=db_object,
            field=db_object._meta.get_field(field_name)
        )
    else:
        raise ValueError("Received adaptor type: '{}', supported adaptors are 'basic', 'ckeditor'")

    inline_adaptor.field_value = field_value

    out = {
        'field_name': field_name,
        'value': field_value,
        'display_type': inline_adaptor.DISPLAY_TYPE,
        'adaptor': inline_adaptor.ADAPTOR_NAME,
        'uuid': field_uuid
    }

    return JsonResponse(out)
