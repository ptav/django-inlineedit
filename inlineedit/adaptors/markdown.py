from django.utils.html import format_html

from inlineedit.adaptors.basic import BasicAdaptor
from markdown import markdown


class MarkdownAdaptor(BasicAdaptor):
    def display_value(self):
        return format_html(markdown(self.db_value()))
