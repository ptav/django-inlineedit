from django.template.library import Library
from django.urls import reverse as reverse_url
from inlineedit.apps import InlineeditConfig

register = Library()


@register.inclusion_tag('inlineedit/default_bevahiour.html', takes_context=False)
def inlineedit_default_script():
    return {
        "inlineedit_endpoint": reverse_url(
            ":".join([InlineeditConfig.name, "inlineedit"])
        )
    }
