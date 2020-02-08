# Django Inline Edit
#
# (c) Pedro Tavares, 2019

from django.conf import settings
from django.utils.html import format_html

try:
    import reversion
    HAS_REVERSION = True
except ImportError:
    HAS_REVERSION = False

try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

try:
    import ckeditor
    HAS_CKEDITOR = True
except ImportError:
    HAS_CKEDITOR = False


def adaptor_factory(model, field, *args, **kwargs):
    """
    Maps the selected adaptor class (or BaseAdaptor if none is selected)

    First *args must be adaptor name or null
    Remaining args and kwargs will be passed to the adaptor class ctor
    """

    field_class = type(field).__name__
    adaptor = args[0] if len(args) else None

    if adaptor and adaptor in ADAPTORS:
        ac = ADAPTORS[adaptor]
    elif field_class in ADAPTORS:
        ac = ADAPTORS[field_class]
    else:
        ac = BaseAdaptor

    return ac(model, field, *args[1:], **kwargs)


class BaseAdaptor(object):
    MODEL = None
    FIELD = None

    def __init__(self, model, field, *args, **kwargs):
        self.MODEL = model
        self.FIELD = field
        self.ARGS = args
        self.KWARGS = kwargs

    def formfield(self):
        "Return form field from model field"
        return self.FIELD.formfield()

    def value(self):
        "Return HTML representation of model field"
        out = getattr(self.MODEL, self.FIELD.attname)

        field_instance = self.FIELD.formfield()
        if hasattr(field_instance, 'choices'):
            out = dict(field_instance.choices).get(out, '--')

        # Apply empty message if field is empty
        if out == "": out = self.empty_message()

        return out

    def empty_message(self):
        field_instance = self.FIELD.formfield()
        return '<span style="opacity:0.5;">Hover to add {}</span>'.format(field_instance.label)


class MarkdownAdaptor(BaseAdaptor):
    def value(self):
        out = getattr(self.MODEL, self.FIELD.attname)
        if out == "": out = self.empty_message()
        return format_html(markdown.markdown(out))

    def format(self):
        return 'html'


class CKEditorAdaptor(BaseAdaptor):
    def formfield(self):
        ff = self.FIELD.formfield()

        config = self.ARGS[0] if len(self.ARGS) else 'default'
        ff.widget = ckeditor.widgets.CKEditorWidget(config_name=config)

        return ff

    def value(self):
        out = getattr(self.MODEL, self.FIELD.attname)
        if out == "": out = self.empty_message()
        return format_html(out)


# List of builtin adaptors
#

ADAPTORS = {
    'markdown': MarkdownAdaptor,
    'ckeditor': CKEditorAdaptor,
}
