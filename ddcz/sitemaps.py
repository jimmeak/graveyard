"""
Sitemap definitions for the sitemap.xml framework.

Important: these Sitemap classes are never invoked during a normal web
request. They are rendered offline by `manage.py warmsitemap` (see
`ddcz/management/commands/warmsitemap.py`) and the resulting XML is cached;
the public `ddcz/views/sitemap.py` views only ever read that cache. This
keeps the (potentially expensive) enumeration of all approved creations
off the request path entirely.
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .creations import ApprovalChoices
from .models import CreativePage

# Priority bands: every creation must outrank every non-creation page, and
# creations are further weighted by their star rating (0-6, see
# ddcz/creations.py RATING_DESCRIPTIONS; 6 is reserved for contest winners).
STATIC_PAGE_PRIORITY = 0.3
LISTING_PAGE_PRIORITY = 0.4
CREATION_BASE_PRIORITY = 0.5
CREATION_RATING_STEP = 0.05

SITEMAP_CACHE_KEY_PREFIX = "sitemap"


def sitemap_index_cache_key():
    return f"{SITEMAP_CACHE_KEY_PREFIX}:index"


def sitemap_section_cache_key(section, page=1):
    return f"{SITEMAP_CACHE_KEY_PREFIX}:{section}:p{page}"


class StaticViewSitemap(Sitemap):
    """Editorial and other static/dynamic public pages that aren't tied to a model."""

    # (url_name, priority, changefreq)
    PAGES = [
        ("news", LISTING_PAGE_PRIORITY, "daily"),
        ("newsfeed", LISTING_PAGE_PRIORITY, "daily"),
        ("users-list", LISTING_PAGE_PRIORITY, "weekly"),
        ("links-list", LISTING_PAGE_PRIORITY, "weekly"),
        ("phorum-list", LISTING_PAGE_PRIORITY, "daily"),
        ("tavern-list", LISTING_PAGE_PRIORITY, "weekly"),
        ("dating", LISTING_PAGE_PRIORITY, "weekly"),
        ("market", LISTING_PAGE_PRIORITY, "weekly"),
        ("postal-service", LISTING_PAGE_PRIORITY, "monthly"),
        ("about-drd", STATIC_PAGE_PRIORITY, "yearly"),
        ("website-manual", STATIC_PAGE_PRIORITY, "yearly"),
        ("faq", STATIC_PAGE_PRIORITY, "yearly"),
        ("web-authors-and-editors", STATIC_PAGE_PRIORITY, "yearly"),
    ]

    def items(self):
        return self.PAGES

    def location(self, item):
        url_name, _, _ = item
        return reverse(f"ddcz:{url_name}")

    def priority(self, item):
        _, priority, _ = item
        return priority

    def changefreq(self, item):
        _, _, changefreq = item
        return changefreq


class CreativePageListSitemap(Sitemap):
    """The /rubriky/<slug>/ listing page for every registered CreativePage."""

    priority = LISTING_PAGE_PRIORITY
    changefreq = "weekly"

    def items(self):
        return list(CreativePage.objects.all())

    def location(self, page):
        return reverse("ddcz:creation-list", kwargs={"creative_page_slug": page.slug})


class CreationSitemap(Sitemap):
    """
    Every approved creation across all CreativePages.

    Mirrors the enumeration in `ddcz/feeds.py` (CompleteNewsFeed.items), but
    without the RSS_LATEST_ITEMS_COUNT cap, since a sitemap wants everything.
    """

    changefreq = (
        "yearly"  # creations don't change after publishing (no `modified` field)
    )

    def items(self):
        items = []
        for entry in CreativePage.get_all_models():
            model, page = entry["model"], entry["page"]
            qs = model.objects.filter(is_published=ApprovalChoices.APPROVED.value)
            if model.SHARED_BETWEEN_CREATIVE_PAGES:
                qs = qs.filter(creative_page_slug=page.slug)
            for creation in qs.order_by("-published").iterator():
                # get_absolute_url() requires .creative_page to be attached
                creation.creative_page = page
                items.append(creation)
        return items

    def location(self, item):
        return item.get_absolute_url()

    def lastmod(self, item):
        return item.published

    def priority(self, item):
        rating = max(0, min(int(item.rating or 0), 6))
        return round(CREATION_BASE_PRIORITY + CREATION_RATING_STEP * rating, 2)


SITEMAPS = {
    "static": StaticViewSitemap,
    "pages": CreativePageListSitemap,
    "creations": CreationSitemap,
}
