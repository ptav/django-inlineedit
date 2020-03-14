# Django Inline Edit
#
# (c) Pedro Tavares, 2019-2020

from django.conf import settings

from .basic import BasicAdaptor
from .ckeditor import CKEditorAdaptor
from .markdown import MarkdownAdaptor


__all__ = [
    BasicAdaptor,
    CKEditorAdaptor,
    MarkdownAdaptor,

]

_ADAPTORS_ = __all__
if hasattr(settings, 'DJANGO_INLINEEDIT_ADAPTORS'):
    _ADAPTORS_ += settings.DJANGO_INLINEEDIT_ADAPTORS

_ADAPTOR_LOOKUP_ = dict([(a.ADAPTOR_NAME,a) for a in _ADAPTORS_])


def get_adaptor_class(adaptor):
    if adaptor == "":
        return  
    elif adaptor in _ADAPTOR_LOOKUP_: 
        return _ADAPTOR_LOOKUP_.get(adaptor)
    else:
        raise ValueError("Adaptor type '{}' not supported".format(adaptor))