# coding: utf-8
from django import template
from confirmanager.utils import get_absolute_url


register = template.Library()


@register.filter
def append_domain(arg):
    return get_absolute_url(arg)