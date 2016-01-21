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
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet
from datetime import datetime
from wagtail.wagtailcore import blocks
from django.utils import timezone


class LinkFields(models.Model):
    description = RichTextField(
        blank=True,
        help_text='brief description of the event',
    )
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
        FieldPanel('description'),
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
    ]

    class Meta:
        abstract = True


class RelatedLink(LinkFields):
    panels = [
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


#class Speaker(models.Model):

class Logo(models.Model, index.Indexed):
    name = models.CharField(max_length = 100, blank=True)
    link = models.URLField("Logo link",
        blank=True,
        null=True,
        help_text='Set an external link in order to point to the logo web site',
    )
    icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
  
    panels = [
        FieldPanel('name'),
        FieldPanel('link'),
        ImageChooserPanel('icon'),
    ]

    class Meta:
        abstract = True

class LogoYourself(Logo):
    panels = [
        MultiFieldPanel(Logo.panels, "Logo"),
        ]
    
    class Meta:
        abstract = True

class HomePage(Page):
    body = RichTextField(blank=True)
    intro = RichTextField(blank=True)
    credit = RichTextField(blank=True)
    image = StreamField([
        ('name', blocks.CharBlock(help_text="title of your logo")),
        ('link', blocks.URLBlock(help_text="url to your website")),
        ('img', ImageChooserBlock()),
    ], blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        StreamFieldPanel('image'),
        FieldPanel('credit'),
        FieldPanel('body'),
        InlinePanel('related_links', label="Related events"),
        #InlinePanel('your_logo', label="Logo"),
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
    btn_txt = models.CharField(max_length = 30, default="S'inscrire")
    btn_link = models.URLField(default="http://www.open-source-innovation-spring.org")
    
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
        InlinePanel('logo', label="logo"),
        FieldPanel('body'),
        FieldRowPanel([
            FieldPanel('btn_txt', classname="col6"),
            FieldPanel('btn_link', classname="col6"),
        ]),
    ]


class EventsRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('HomePage', related_name='related_links')

class LogoMaker(Orderable, LogoYourself):
    page = ParentalKey('EventsPage', related_name='logo')
