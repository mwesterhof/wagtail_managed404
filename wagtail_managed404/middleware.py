import re

from django.conf import settings
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.utils.timezone import now

from .models import PageNotFoundEntry


IGNORED_404S = getattr(settings, 'IGNORED_404S', [
    r'^/static/',
    r'^/favicon.ico'
])


class PageNotFoundRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.blacklist_url_patterns = [
            re.compile(string) for string in IGNORED_404S]

    def __call__(self, request):
        url = request.path
        if self._check_url_in_blacklist(url):
            return self.get_response(request)

        else:
            return self.handle_request(request)

    def _check_url_in_blacklist(self, url):
        return any(
            [pattern.match(url) for pattern in self.blacklist_url_patterns])

    def handle_request(self, request):
        url = request.path
        site = request.site

        entry = PageNotFoundEntry.objects.filter(
            site=site, url=url).first()
        if entry:
            entry.hits += 1
            entry.last_hit = now()
            entry.save()

            if entry.redirect_to:
                if entry.permanent:
                    return HttpResponsePermanentRedirect(entry.redirect_to)
                else:
                    return HttpResponseRedirect(entry.redirect_to)

        response = self.get_response(request)
        if response.status_code == 404 and not entry:
            PageNotFoundEntry.objects.create(
                site=site, url=url, last_hit=now())
        return response
