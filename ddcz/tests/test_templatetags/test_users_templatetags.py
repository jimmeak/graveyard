from django.test import TestCase
from django.utils import timezone

from ddcz.models import UserProfile
from ddcz.models.used.users import Rune
from ddcz.templatetags.users import nick_icon, nick_url

# Nick with a caron char (ž) that misencodes into the cp1250 C1 range (\x9e) —
# the exact class of value that used to crash nick_url/nick_icon (Sentry DDCZ-2T).
SPECIAL_NICK = "Keydža"


class NickFilterTest(TestCase):
    def setUp(self):
        super().setUp()
        self.profile = UserProfile.objects.create(nick=SPECIAL_NICK, icon="Keydza.gif")

    def test_nick_url_resolves_special_char_nick(self):
        self.assertEqual(nick_url(SPECIAL_NICK), self.profile.profile_url)

    def test_nick_url_unknown_nick_falls_back(self):
        self.assertEqual(nick_url("nobody-here"), "#")

    def test_nick_icon_resolves_special_char_nick(self):
        self.assertEqual(nick_icon(SPECIAL_NICK), self.profile.icon_url)

    def test_rune_donor_nick_round_trips_and_links(self):
        """donor_nick is now a MisencodedCharField: it must display as true unicode
        and resolve to the donor's profile instead of crashing / linking to '#'."""
        rune = Rune.objects.create(
            donor_id=self.profile.id,
            donor_nick=SPECIAL_NICK,
            receiver_id=self.profile.id,
            receiver_nick=SPECIAL_NICK,
            type="rune",
            graphics=1,
            text="díky",
            date=timezone.now(),
        )
        reloaded = Rune.objects.get(pk=rune.pk)

        self.assertEqual(reloaded.donor_nick, SPECIAL_NICK)
        self.assertEqual(nick_url(reloaded.donor_nick), self.profile.profile_url)
