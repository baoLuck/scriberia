import logging

import httpx
import orjson
from asgiref.sync import sync_to_async
from django.core.handlers.asgi import ASGIRequest
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from server.bot import BOT_TOKEN
from server.models import DoneOffersByUser, Offer, TGUser

logger = logging.getLogger(__name__)


class OffersPage(ListView):
    model = Offer
    template_name = "server/home.html"
    context_object_name = "offers"

    def get_queryset(self):
        return Offer.objects.filter(available=True)


@csrf_exempt
async def check_subscription(request: ASGIRequest):
    if request.method == "POST":
        data = orjson.loads(request.body)

        offer = Offer.objects.get(pk=data.get("pk"))

        tg_id = data.get("tg_id")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember",
                params={"chat_id": "@" + offer.link.rpartition("/")[-1], "user_id": tg_id},
            )

        data = response.json()

        if data["ok"]:
            status = data["result"]["status"]
            if status in ["member", "administrator", "creator"]:
                tg_user = await TGUser.objects.filter(tg_id=tg_id).afirst()

                await DoneOffersByUser.objects.acreate(offer_id=offer.pk, tg_user_id=tg_user.pk)

                tg_user.ton_balance += offer.reward
                await tg_user.asave(update_fields=("ton_balance",))

                return JsonResponse(
                    {
                        "status": "success",
                        "is_subscribed": True,
                        "balance": tg_user.ton_balance,
                    },
                )

        return JsonResponse({"status": "success", "is_subscribed": False})

    return JsonResponse({"status": "error", "error": "Invalid request"}, status=400)


async def show_offers(request: ASGIRequest):
    if request.method == "GET":
        tg_user = await TGUser.objects.aget(tg_id=request.GET.get("tg_id"))

        done_offers = DoneOffersByUser.objects.filter(tg_user_id=tg_user.pk).values_list("offer_id", flat=True)

        available_offers = Offer.objects.filter(available=True).exclude(Q(id__in=done_offers))

        leaderboard_users = TGUser.objects.order_by("-ton_balance")[:50]

        return await sync_to_async(render)(
            request,
            "server/offers.html",
            {
                "offers": available_offers,
                "current_user": tg_user,
                "leaderboard_users": leaderboard_users,
            },
        )

    return JsonResponse({"status": "error", "detail": {"Incorrect method"}})


def show_leaderboard(request: ASGIRequest):
    return render(request, "server/leaderboard.html")


def show_friends(request: ASGIRequest):
    return render(request, "server/friends.html")


def log_js(request):
    message = request.GET.get("message", "")
    logger.info(f"JS log: {message}")

    return JsonResponse({"status": "ok"})
