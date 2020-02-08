from django.shortcuts import render
from django.http import JsonResponse
from django.apps import apps

from . import adaptor_factory, HAS_REVERSION

if HAS_REVERSION:
    import reversion


def inlineedit_form_submit(request):
    "Indicate interest for a particular project"
    if not request.is_ajax() or not request.POST:
        return JsonResponse({'success':False})

    field = request.POST['field']
    id = request.POST['id']
    arg = request.session[id]

    strip = arg.split(".")
    model_class = apps.get_model(strip[0], strip[1])
    obj = model_class.objects.get(pk=strip[3])
    field_name = strip[2]

    setattr(obj, field_name, field)

    if HAS_REVERSION:
        with reversion.create_revision():
            obj.save()
            reversion.set_user(request.user)
            reversion.set_comment(
                "Updated {} {} to {}".format(strip[1], field_name, field)
            )

    else:
        obj.save()

    # Data for updating HTML
    field = obj._meta.get_field(field_name)
    ac = adaptor_factory(obj, field, strip[4])
    field_value = ac.value()
    field_type = ac.format()

    out = {
        'success': True,
        'uuid': id,
        'value': field_value,
        'type': field_type,
    }

    return JsonResponse(out)
