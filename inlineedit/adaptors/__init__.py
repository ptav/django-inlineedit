# Django Inline Edit
#
# (c) Pedro Tavares, 2019-2020

from importlib import import_module
from django.conf import settings

from .basic import BasicAdaptor
from .ckeditor import CKEditorAdaptor, CKEditorImplicitAdaptor
from .markdown import MarkdownAdaptor


_ADAPTOR_LOOKUP_ = {
    'basic': BasicAdaptor,
    'markdown': MarkdownAdaptor,
    'ckeditor': CKEditorAdaptor,
    'ckeditor-implicit': CKEditorImplicitAdaptor,
}


if hasattr(settings, 'INLINEEDIT_ADAPTORS'):
    for key,item in settings.INLINEEDIT_ADAPTORS.items():
        x = item.split('.')
        m = import_module('.'.join(x[:-1]))
        c = getattr(m, x[-1])
        _ADAPTOR_LOOKUP_[key] = c


def _get_adaptor_class_(adaptor):
    if adaptor == "":
        return  
    elif adaptor in _ADAPTOR_LOOKUP_: 
        return _ADAPTOR_LOOKUP_.get(adaptor)
    else:
        raise ValueError("Adaptor type '{}' not supported".format(adaptor))