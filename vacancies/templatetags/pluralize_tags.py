from django import template

from jobs_project.morph import morph

register = template.Library()


@register.filter
def pluralize(number, word):
    parsed = morph.parse(word)
    if isinstance(parsed, list):
        result = parsed[0].make_agree_with_number(number)
        return result.word
    return word
