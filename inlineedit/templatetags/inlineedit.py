from django import template, forms

from .. import adaptor_factory


register = template.Library()


@register.inclusion_tag('inlineedit/default.html', takes_context=True)
def inlineedit(context, arg, *args, **kwargs):
    "Render editable field"
    strip = arg.split('.')
    if len(strip) < 2:
        raise template.exceptions.TemplateSyntaxError("inlineedit invalid argument \"{}\": must be of the form \"model.field\"".format(arg))

    model_name = strip[0]
    field_name = strip[1]

    obj = context[model_name]
    fld = obj._meta.get_field(field_name)

    ac = adaptor_factory(obj, fld, *args, **kwargs)
    field_render = ac.value()

    adaptor = args[0] if len(args) else None

    uuid = 'hash' + str(hash(arg)) # must be string to avoid localisation #uuid1().hex
    context.request.session[uuid] = "{}.{}.{}.{}".format(
        obj._meta.label,
        fld.attname,
        obj.pk,
        adaptor)

    class AuxForm(forms.Form):
        id = forms.CharField(max_length=32, widget=forms.HiddenInput())
        field = ac.formfield()

    # Field attribute must be added dynamically so that each
    # has a different HTML 'id' (relevant for CKEditor for example)

    form = AuxForm({
        'field': getattr(obj, field_name),
        'id': uuid},
        auto_id=arg.replace('.','__') + '__%s')

    return {
        'form': form,
        'value': field_render,
        'uuid': uuid,
    }
