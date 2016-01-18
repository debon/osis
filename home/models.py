from __future__ import unicode_literals

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import (FieldPanel,
                                                FieldRowPanel,
                                                InlinePanel,
                                                MultiFieldPanel,
                                                PageChooserPanel,
                                                StreamFieldPanel)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet
from datetime import datetime
from wagtail.wagtailcore import blocks
from django.utils import timezone


class LinkFields(models.Model):
    link_external = models.URLField(
        "External link",
        blank=True,
        null=True,
        help_text='Set an external link if you want to describe the event from an other web site',
    )
    link_page = models.ForeignKey(
        'home.EventsPage',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+',
        help_text='Choose an existing page (event must have already been created)',
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
    ]

    class Meta:
        abstract = True

#class Location(models.Model):
#    city = models.CharField(max_length = 20, blank=True)
#    place = models.CharField(max_length = 20, blank=True)
#    place_link = models.URLField(blank = True)
    

class RelatedLink(LinkFields):
    #title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        #FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


class HomePage(Page):
    body = RichTextField(blank=True)
    intro = RichTextField(blank=True)
    credit = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('credit'),
        FieldPanel('body'),
        InlinePanel('related_links', label="Related events"),
    ]


class EventsPage(Page):
    
    # Database fields

    date_start = models.DateTimeField(default=timezone.now, blank=True)
    date_stop = models.DateTimeField(default=timezone.now, blank=True)
    tag = models.CharField(max_length = 25)
    city = models.CharField(max_length = 20, blank=True)
    place = models.CharField(max_length = 20, blank=True)
    place_link = models.URLField(blank = True)
    main_title = models.CharField(max_length = 255, default="Event Description")
    main_title_link = models.URLField(blank=True)
    body = RichTextField(blank=True)
    
    #TO DO configure a set of choices for design presentation :
    # Schedules -> Program -> Speakers -> Topics

    # Search index configuration

    search_fields = Page.search_fields + (
        index.SearchField('tag'),
        index.SearchField('city'),
        index.FilterField('date_start'),
    )

    # Editor panels configuration
    
    content_panels = Page.content_panels + [
        FieldRowPanel([
            FieldPanel('date_start', classname="col3"),
            FieldPanel('date_stop', classname="col3"),
            FieldPanel('tag', classname="col3"),
            FieldPanel('city', classname="col3"),
        ]),
        FieldRowPanel([
            FieldPanel('place', classname="col6"),
            FieldPanel('place_link', classname="col6"),
        ]),
        FieldRowPanel([
            FieldPanel('main_title', classname="col6"),
            FieldPanel('main_title_link', classname="col6"),
        ]),
        FieldPanel('body'),
    ]


class EventsRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('HomePage', related_name='related_links')

