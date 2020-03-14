from django.utils.html import format_html

from inlineedit.adaptors.basic import BasicAdaptor
from markdown import markdown


class MarkdownAdaptor(BasicAdaptor):
    ADAPTOR_NAME = "markdown"

    def display_value(self) -> str:
        return format_html(markdown(self.db_value()))
