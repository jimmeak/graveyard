from django.core.cache import cache
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from ..sitemaps import sitemap_index_cache_key, sitemap_section_cache_key

# Sitemap XML is precomputed offline by `manage.py warmsitemap` (run on every
# deploy and on a schedule -- see Procfile) and stored in cache. These views
# only ever read that cache; they never compute a sitemap in-request. A miss
# means the warm-up hasn't run yet (or the cache was flushed) -- rather than
# serve a wrong/truncated sitemap, tell the crawler to come back shortly.
CACHE_MISS_RETRY_AFTER_SECONDS = 300


def _serve_or_503(xml):
    if xml is None:
        return HttpResponse(
            status=503, headers={"Retry-After": CACHE_MISS_RETRY_AFTER_SECONDS}
        )
    return HttpResponse(xml, content_type="application/xml")


@require_http_methods(["HEAD", "GET"])
def sitemap_index(request):
    return _serve_or_503(cache.get(sitemap_index_cache_key()))


@require_http_methods(["HEAD", "GET"])
def sitemap_section(request, section):
    page = request.GET.get("p", 1)
    return _serve_or_503(cache.get(sitemap_section_cache_key(section, page)))
