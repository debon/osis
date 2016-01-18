from django import template
from home.models import *

register = template.Library()

@register.inclusion_tag('home/tags/events.html', takes_context=True)
def events(context):
    return {
        'events': Events.objects.all(),
        'request': context['request'],
    }
