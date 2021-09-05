import logging
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from ..models import UserProfile, Letter
from ..text import misencode

FORM_DELETE = 1
FORM_SEND = 2
FORM_REPLY = 4

DEFAULT_LIMIT = 10
DEFAULT_PAGE = 1

logger = logging.getLogger(__name__)


@login_required
@require_http_methods(["HEAD", "GET", "POST"])
def postal_service(request):
    if request.method == "POST":
        return handle_postal_service_post_request(request)

    nick = request.user.profile.nick
    per_page = int(request.GET.get("l", DEFAULT_LIMIT))
    page = int(request.GET.get("z_s", DEFAULT_PAGE))

    letters = Letter.objects.filter(
        ((Q(receiver=nick) | Q(sender=nick)) & Q(visibility=3))
        | (Q(receiver=nick) & Q(visibility=2))
        | (Q(sender=nick) & Q(visibility=1))
    ).order_by("-date")

    box_occupancy = Letter.objects.filter(
        (Q(receiver=nick) | Q(sender=nick)) & Q(visibility=1)
    ).count()

    paginator = Paginator(letters, per_page)
    letters = paginator.get_page(page)

    return render(
        request,
        "postal_service/postal_office.html",
        {
            "reply_id": FORM_REPLY,
            "send_id": FORM_SEND,
            "delete_id": FORM_DELETE,
            "letters": letters,
            "per_page": per_page if per_page != DEFAULT_LIMIT else False,
            "box_occupancy": box_occupancy,
        },
    )


def handle_postal_service_post_request(request):
    fid = int(request.POST.get("fid"))
    if fid == FORM_SEND:
        receiver_nick = request.POST.get("whom")
        try:
            Letter.objects.create(
                receiver=UserProfile.objects.get(nick=misencode(receiver_nick)).nick,
                sender=request.user.userprofile.nick,
                text=request.POST.get("text"),
                date=datetime.now(),
                visibility=3,
            )
            return HttpResponseRedirect(reverse("ddcz:postal-service"))
        except UserProfile.DoesNotExist:
            logger.info(f"Letter receiver {receiver_nick} could not be found")
            messages.error(
                f"Helimardovi se nepodařilo nalézt nikoho se jménem f{receiver_nick}. Ověřte prosím jeho práci v seznamu uživatelů a případně dejte vědět, zda si zaslouží nášup při dalším krmení."
            )
            return HttpResponseRedirect(reverse("ddcz:postal-service"))

    elif fid == FORM_DELETE:
        try:
            Letter.objects.filter(pk=request.POST.get("id", 0)).update(visibility=0)
            return HttpResponseRedirect(reverse("ddcz:postal-service"))
        except Letter.DoesNotExist:
            letter_id = request.POST.get("id")
            user = request.user.userprofile.nick
            logger.info(
                f"There has been an attempt to delete a letter with non existing id {letter_id} by user {user}"
            )
            messages.error(
                "Ať koukáme, jak koukáme, tento dopis ke spálení nemůžeme nalézt."
            )
            return HttpResponseRedirect(reverse("ddcz:postal-service"))
