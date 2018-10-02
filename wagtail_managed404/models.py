from django.db import models
from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, PageChooserPanel)
from wagtail.core.models import Page, Site


class PageNotFoundEntry(models.Model):
    site = models.ForeignKey(
        Site, related_name='pagenotfound_entries', on_delete=models.CASCADE)

    url = models.CharField(max_length=200)
    redirect_to_url = models.CharField(max_length=200, null=True, blank=True)
    redirect_to_page = models.ForeignKey(
        Page, on_delete=models.CASCADE, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    last_hit = models.DateTimeField()
    hits = models.PositiveIntegerField(default=1)
    permanent = models.BooleanField(default=False)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('site'),
                FieldPanel('url'),
            ], heading='entry'),
        MultiFieldPanel(
            [
                FieldPanel('last_hit'),
                FieldPanel('hits'),
            ], heading='general', classname='collapsible'),
        MultiFieldPanel(
            [
                PageChooserPanel('redirect_to_page'),
                FieldPanel('redirect_to_url'),
                FieldPanel('permanent'),
            ], heading='redirect', classname='collapsible'),
    ]

    @property
    def redirect_to(self):
        if self.redirect_to_page:
            return self.redirect_to_page.url
        return self.redirect_to_url

    def __str__(self):
        return self.url

    class Meta:
        verbose_name_plural = "page not found redirects"
        ordering = ('-hits',)
