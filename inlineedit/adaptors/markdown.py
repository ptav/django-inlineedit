from inlineedit.adaptors.basic import InlineFieldAdaptor
from markdown import markdown


class MarkdownAdaptor(InlineFieldAdaptor):
    DISPLAY_TYPE = "html"
    ADAPTOR_NAME = "markdown"
