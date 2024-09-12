import json
import logging

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.db.models import Q, Window, F
from django.db.models.functions import RowNumber


from .bot import BOT_TOKEN
from .models import *


class OffersPage(ListView):
    model = Offer
    template_name = 'server/home.html'
    context_object_name = 'offers'

    def get_queryset(self):
        return Offer.objects.filter(available=True)


class ManifestPage(ListView):
    template_name = 'tonconnect-manifest.json'


@csrf_exempt
def check_subscription(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        offer = Offer.objects.get(pk=data.get('pk'))
        offer_name = "@" + offer.link.rpartition('/')[-1]
        tg_id = data.get('tg_id')

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"
        params = {
            'chat_id': offer_name,
            'user_id': tg_id
        }

        response = requests.get(url, params=params)
        data = response.json()
        if data['ok']:
            status = data['result']['status']
            if status in ['member', 'administrator', 'creator']:
                tg_user = TGUser.objects.filter(tg_id=tg_id)[0]
                done_offer = DoneOffersByUser(offer_id=offer.pk, tg_user_id=tg_user.pk)
                done_offer.save()
                tg_user.ton_balance += offer.ton_reward
                tg_user.scribe_balance += offer.scribes_reward
                tg_user.save()
                offer.current_subscriptions += 1
                if offer.current_subscriptions >= offer.max_subscriptions:
                    offer.available = False
                offer.save()

                return JsonResponse({'status': 'success', 'is_subscribed': True, 'ton_balance': tg_user.ton_balance,
                                     'scribe_balance': tg_user.scribe_balance})

        return JsonResponse({'status': 'success', 'is_subscribed': False})

    return JsonResponse({'status': 'error', 'error': 'Invalid request'}, status=400)


def show_offers(request):
    if request.method == 'GET':
        tg_user = TGUser.objects.get(tg_id=request.GET.get('tg_id'))
        done_offers = DoneOffersByUser.objects.filter(tg_user_id=tg_user.pk).values_list('offer_id', flat=True)
        available = Offer.objects.exclude(Q(id__in=done_offers) | Q(available=False))
        leaderboard_users = TGUser.objects.order_by('-ton_balance')[:50]
        sorted_records = TGUser.objects.annotate(
            row_number=Window(
                expression=RowNumber(),
                order_by=F('ton_balance').desc()
            )
        )
        print(sorted_records)
        return render(request, 'server/offers.html',
                      {'offers': available, 'current_user': tg_user, 'leaderboard_users': leaderboard_users})


def show_leaderboard(request):
    print("leader")
    return render(request, 'server/leaderboard.html')


def show_friends(request):
    print("friend")
    return render(request, 'server/friends.html')


logger = logging.getLogger(__name__)


def log_js(request):
    message = request.GET.get('message', '')
    logger.info(f'JS log: {message}')
    return JsonResponse({'status': 'ok'})

