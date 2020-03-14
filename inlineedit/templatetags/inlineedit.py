from django.template.library import Library
from django.template.exceptions import TemplateSyntaxError
from django.db.models import Model as DjangoModel, Field as DjangoField
from django.forms import Form as DjangoForm
from django.forms.widgets import HiddenInput
from django.forms import fields

from ..adaptors import get_adaptor_class


register = Library()


@register.inclusion_tag('inlineedit/default.html', takes_context=True)
def inlineedit(context, field_info, adaptor="basic", *args):
    try:
        object_name, field_name = tuple(field_info.split('.'))
    except ValueError:
        raise TemplateSyntaxError('inlineedit invalid argument '
                                  '"{}": must be of the form '
                                  '"model.field"'.format(field_info))

    object_model: DjangoModel = context[object_name]
    model_name = object_model._meta.label

    # noinspection PyProtectedMember
    field: DjangoField = object_model._meta.get_field(field_name)

    adaptor_class = get_adaptor_class(adaptor)
    adaptor_obj = adaptor_class(object_model, field, *args)

    uuid = str(hash(field_info))
    
    # noinspection PyProtectedMember
    context.request.session[uuid] = "{}.{}.{}.{}".format(
        model_name,
        field_name,
        object_model.pk,
        adaptor
    )

    class _InlineeditForm(DjangoForm):
        uuid = fields.CharField(max_length=32, widget=HiddenInput())
        field = adaptor_obj.form_field()

    # Field attribute must be added dynamically so that each
    # has a different HTML 'id' (relevant for CKEditor)

    form = _InlineeditForm(
        {'field': adaptor_obj.db_value(), 'uuid': uuid},
        auto_id=field_info.replace('.', '__') + '__%s'
    )

    value = adaptor_obj.display_value()
    empty_msg = "" if value else adaptor_obj.empty_message()

    return {
        'form': form,
        'value': value,
        'empty_message': empty_msg,
        'adaptor': adaptor,
        'uuid': uuid,
    }
