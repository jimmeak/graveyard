import xml.etree.ElementTree as ET

from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from ddcz.creations import ApprovalChoices
from ddcz.models import CommonArticle
from ddcz.tests.model_generator import get_valid_article_chain

SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def parse_urlset(xml_bytes):
    root = ET.fromstring(xml_bytes)
    urls = []
    for url_el in root.findall(f"{SITEMAP_NS}url"):
        loc = url_el.find(f"{SITEMAP_NS}loc").text
        priority_el = url_el.find(f"{SITEMAP_NS}priority")
        urls.append(
            {
                "loc": loc,
                "priority": float(priority_el.text)
                if priority_el is not None
                else None,
            }
        )
    return urls


class SitemapTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        super().setUp()
        cache.clear()

        article_chain = get_valid_article_chain()
        self.user_profile = article_chain["user"]
        self.author = article_chain["author"]
        self.article = article_chain["article"]
        self.article.rating = 5
        self.user_profile.save()
        self.author.save()
        self.article.save()

        self.unapproved_article = CommonArticle.objects.create(
            name="Waiting Article",
            is_published=ApprovalChoices.WAITING.value,
            creative_page_slug="clanky",
            text="Not approved yet",
        )

    def tearDown(self):
        cache.clear()
        super().tearDown()

    def test_cold_cache_returns_503(self):
        response = self.client.get(reverse("ddcz:sitemap-index"))
        self.assertEqual(response.status_code, 503)
        self.assertIn("Retry-After", response.headers)

    def test_warmed_index_references_sections(self):
        call_command("warmsitemap")

        response = self.client.get(reverse("ddcz:sitemap-index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertIn(b"sitemap-static.xml", response.content)
        self.assertIn(b"sitemap-pages.xml", response.content)
        self.assertIn(b"sitemap-creations.xml", response.content)

    def test_creations_section_includes_only_approved(self):
        call_command("warmsitemap")

        response = self.client.get(
            reverse("ddcz:sitemap-section", kwargs={"section": "creations"})
        )
        self.assertEqual(response.status_code, 200)

        approved_url = reverse(
            "ddcz:creation-detail",
            kwargs={
                "creative_page_slug": "clanky",
                "creation_id": self.article.pk,
                "creation_slug": self.article.get_slug(),
            },
        )
        waiting_url = reverse(
            "ddcz:creation-detail",
            kwargs={
                "creative_page_slug": "clanky",
                "creation_id": self.unapproved_article.pk,
                "creation_slug": self.unapproved_article.get_slug(),
            },
        )

        urls = parse_urlset(response.content)
        locs = [entry["loc"] for entry in urls]
        self.assertTrue(any(loc.endswith(approved_url) for loc in locs))
        self.assertFalse(any(loc.endswith(waiting_url) for loc in locs))

    def test_creations_outrank_static_pages_by_rating(self):
        call_command("warmsitemap")

        static_response = self.client.get(
            reverse("ddcz:sitemap-section", kwargs={"section": "static"})
        )
        creations_response = self.client.get(
            reverse("ddcz:sitemap-section", kwargs={"section": "creations"})
        )

        static_priorities = [
            entry["priority"] for entry in parse_urlset(static_response.content)
        ]
        creation_priorities = [
            entry["priority"] for entry in parse_urlset(creations_response.content)
        ]

        self.assertTrue(creation_priorities)
        self.assertTrue(static_priorities)
        # Every article must strictly outrank every non-article page.
        self.assertGreater(min(creation_priorities), max(static_priorities))
        # rating=5 -> 0.5 + 0.05 * 5 == 0.75
        self.assertIn(0.75, creation_priorities)
