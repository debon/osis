from django import template
from django.conf import settings
from home.models import *

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_site_root(context):
    return context['request'].site.root_page


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


@register.inclusion_tag('home/tags/top_menu.html', takes_context=True)
def top_menu(context, parent, calling_page=None):
    #add
    root = get_site_root(context)
    try:
        is_root_page = (root.id == calling_page.id)
    except:
        is_root_page = False
    #end add
    menuitems = parent.get_children().live().in_menu()
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        menuitem.active = (calling_page.url.startswith(menuitem.url)
                           if calling_page else False)
    return {
        'calling_page': calling_page,
        'parent': parent,
        'menuitems': menuitems,
        #add
        'is_root_page': is_root_page,
        #end add
        'request': context['request'],
    }


@register.inclusion_tag('home/tags/top_menu_children.html', takes_context=True)
def top_menu_children(context, parent, sub=False, level=0):
    menuitems_children = parent.get_children()
    menuitems_children = menuitems_children.live().in_menu()
    
    for menuitem in menuitems_children:
        menuitem.show_dropdown = has_menu_children(menuitem)

    levelstr = "".join('a' for i in range(level))
    level += 1

    return {
        'parent': parent,
        'menuitems_children': menuitems_children,
        'sub': sub,
        'level': level,
        'levelstr': levelstr,
        'request': context['request'],
    }

@register.inclusion_tag('home/tags/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    self = context.get('self')
    if self is None or self.depth <= 2:
        # When on the home page, displaying breadcrumbs is irrelevant.
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(
            self, inclusive=True).filter(depth__gt=2)
    return {
        'ancestors': ancestors,
        'request': context['request'],
    }
