from re import IGNORECASE, compile, escape as rescape

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def highlight(text, search):
    rgx = compile(rescape(search), IGNORECASE)
    return mark_safe(
        rgx.sub(
            lambda m: '<b class="text text-danger">{}</b>'.format(m.group()),
            text
        )
    )
