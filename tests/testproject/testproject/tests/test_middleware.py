import unittest

from django.test import Client

from wagtail.core.models import Page
from wagtail_managed404.models import PageNotFoundEntry


class TestMiddleware(unittest.TestCase):
    """Tests for `wagtail_app_pages` package."""

    def setUp(self):
        self.client = Client()
        self.invalid_url = '/definitely_not_an_actual_url/'
        self.redirect_to_url = '/much_better_url/'
        self.redirect_to_page = Page.objects.get(depth=2)

    def test_redirect_to_url(self):
        PageNotFoundEntry.objects.all().delete()
        entry = self._trigger_404()
        entry.redirect_to_url = self.redirect_to_url
        entry.save()
        self._validate_redirect(self.invalid_url, self.redirect_to_url)

    def test_redirect_to_page(self):
        PageNotFoundEntry.objects.all().delete()
        entry = self._trigger_404()
        entry.redirect_to_page = self.redirect_to_page
        entry.save()
        self._validate_redirect(self.invalid_url, self.redirect_to_page.url)

    def _trigger_404(self):
        response = self.client.get(self.invalid_url)
        self.assertEquals(response.status_code, 404)

        entries = PageNotFoundEntry.objects.filter(url=self.invalid_url)
        self.assertEquals(entries.count(), 1)
        return entries.first()

    def _validate_redirect(self, source_url, target_url):
        response = self.client.get(source_url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, target_url)
