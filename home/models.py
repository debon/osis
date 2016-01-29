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

# Links that point to events pages from home page

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
        'wagtailcore.Page',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+',
        help_text='Choose an existing page (must have already been created)',
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


# Topics of the year

class Topics(models.Model):
    subject = models.CharField(max_length = 100, blank=True)
    
    panels = [
        FieldPanel('subject'),
    ]

    class Meta:
        abstract=True


# Supports Links for footer

class Supports(models.Model):
    name = models.CharField(max_length = 254, blank=True)
    link = models.URLField("support link", blank=True, null=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('link'),
    ]

    class Meta:
        abstract=True


class SupportTupple(Supports):
    panels = [
        MultiFieldPanel(Supports.panels, "supports"),
    ]
    
    class Meta:
        abstract=True
    

#Load an image for events or home page

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
    category = models.CharField(max_length = 100,
                                default="Organizer",
                                help_text="Organizer, Main_Organizer, Support, Coordinator, Follower",
                                blank=True,
    )
  
    panels = [
        FieldPanel('name'),
        FieldPanel('link'),
        ImageChooserPanel('icon'),
        FieldPanel('category'),
    ]

    class Meta:
        abstract = True

class LogoYourself(Logo):
    panels = [
        MultiFieldPanel(Logo.panels, "Logo"),
        ]
    
    class Meta:
        abstract = True


# Model for a speaker or just someone important

class Person(Page):
    firstname = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=254, blank=True)
    job = models.CharField(max_length=254, blank=True)
    spot = models.CharField(max_length=200, blank=True)
    spot_link = models.URLField(max_length=254, blank=True)
    mail = models.EmailField(max_length=254, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    pict = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    
    content_panels = Page.content_panels + [
        FieldRowPanel([
            FieldPanel('firstname', classname="col4"),
            FieldPanel('name', classname="col4"),
            FieldPanel('job', classname="col4"),
        ]),
        FieldRowPanel([
            FieldPanel('spot', classname="col6"),
            FieldPanel('spot_link', classname="col6"),
        ]),
        FieldRowPanel([
            FieldPanel('mail', classname="col6"),
            FieldPanel('phone', classname="col6"),
        ]),
        ImageChooserPanel('pict'),
    ]


class Group(Page):
    content_panels = Page.content_panels + [
        InlinePanel('speakers', label="speakers"),
    ]


class Talk(models.Model):
    time_start = models.TimeField(blank=True)
    time_end = models.TimeField(blank=True, null=True)
    name = models.CharField(max_length=254, blank=True)
    resume = RichTextField(blank=True)
    speaker = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+',
        help_text='Choose an existing person or group (must have already been created)',
    )

    panels = [
        FieldPanel('name'),
        FieldRowPanel([
            FieldPanel('time_start', classname="col6"),
            FieldPanel('time_end', classname="col6"),
        ]),
        FieldPanel('resume'),
        PageChooserPanel('speaker'),
    ]

    class Meta:
        abstract=True


class Talks(Talk):
    panels = [
        MultiFieldPanel(Talk.panels, "talks"),
    ]
    
    class Meta:
        abstract=True


class Section(models.Model):
    time_start = models.TimeField(blank=True)
    time_end = models.TimeField(blank=True, null=True)
    section_name = models.CharField(max_length=254, blank=True)

    panels = [
        FieldPanel('section_name'),
        FieldRowPanel([
            FieldPanel('time_start', classname="col6"),
            FieldPanel('time_end', classname="col6"),
        ]),
    ]

    class Meta:
        abstract=True


class SectionZip(Section):
    panels = [
        MultiFieldPanel(Section.panels, "division"),
    ]

    class Meta:
        abstract=True


class ProgramPage(Page):
    content_panels = Page.content_panels + [
        InlinePanel('division', label="division"),
        InlinePanel('talks', label="talks"),
    ]


class HomePage(Page):
    body = RichTextField(blank=True)
    dates = RichTextField(blank=True)
    ct_name = models.CharField(max_length = 100, blank = True)
    ct_mail = models.EmailField(max_length = 254, blank = True)
    image = StreamField([
        ('name', blocks.CharBlock(help_text="title of your logo")),
        ('link', blocks.URLBlock(help_text="url to your website")),
        ('img', ImageChooserBlock()),
    ], blank=True)

    def get_organizer(self):
        return self.logo.filter(category="Main_Organizer")

    def get_support(self):
        return self.logo.filter(category="Support")
    
    def get_coordinator(self):
        return self.logo.filter(category="Coordinator")

    def get_follower(self):
        return self.logo.filter(category="Follower")

    content_panels = Page.content_panels + [
        InlinePanel('topics', label="Topics"),
        FieldPanel('dates'),
       # StreamFieldPanel('image'),
        FieldPanel('body'),
        InlinePanel('related_links', label="Related events"),
        FieldPanel('ct_name'),
        FieldPanel('ct_mail'),
        InlinePanel('supports', label="supports"),
        InlinePanel('logo', label="Logo"),
    ]


class MainPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
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
    
    def get_home(self):
        return self.get_ancestors().type(HomePage).last().specific
    
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
        InlinePanel('program', label="program"),
        InlinePanel('logo', label="logo"),
        FieldPanel('body'),
        FieldRowPanel([
            FieldPanel('btn_txt', classname="col6"),
            FieldPanel('btn_link', classname="col6"),
        ]),
    ]


class LogoHome(Orderable, LogoYourself):
    page = ParentalKey('home.HomePage', related_name='logo')

class EventsRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('home.HomePage', related_name='related_links')

class LogoEvents(Orderable, LogoYourself):
    page = ParentalKey('home.EventsPage', related_name='logo')

class SupportsHome(Orderable, SupportTupple):
    page = ParentalKey('home.HomePage', related_name='supports')

class TopicsHome(Orderable, Topics):
    page = ParentalKey('home.HomePage', related_name='topics')

class TalkProg(Orderable, Talks):
    page = ParentalKey('home.ProgramPage', related_name="talks")

class SecProg(Orderable, SectionZip):
    page = ParentalKey('home.ProgramPage', related_name="division")

class ProgramRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('home.EventsPage', related_name='program')

class PersonGroup(Orderable, RelatedLink):
    page = ParentalKey('home.Group', related_name='speakers')

