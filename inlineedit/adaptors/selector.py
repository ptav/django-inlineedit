from django.conf import settings

from . import basic, markdown, ckeditor


ADAPTORS = [
    basic.InlineFieldAdaptor,
    markdown.MarkdownAdaptor,
    ckeditor.CKEditorFieldAdaptor,
]


if hasattr(settings, 'DJANGO_INLINEEDIT_ADAPTORS'):
    ADAPTORS += DJANGO_INLINEEDIT_ADAPTORS


_ADAPTOR_LOOKUP_ = dict([(a.ADAPTOR_NAME,a) for a in ADAPTORS])


def get_adaptor_class(adaptor):
    if adaptor == "":
        return  
    elif adaptor in _ADAPTOR_LOOKUP_: 
        return _ADAPTOR_LOOKUP_.get(adaptor)
    else:
        raise ValueError("Adaptor type '{}' not supported".format(adaptor))
