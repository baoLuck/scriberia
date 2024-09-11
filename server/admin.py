from django.contrib import admin

from server.models import Offer, TGUser, DoneOffersByUser


class OffersAdminPanel(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'reward', 'link', 'available')
    search_fields = ('name',)
    list_editable = ('available', 'link')


class TGUserAdminPanel(admin.ModelAdmin):
    list_display = ('id', 'tg_id', 'tg_username', 'ton_balance', 'scribe_balance')
    search_fields = ('tg_username',)
    list_editable = ('ton_balance', 'scribe_balance')


class DoneOffersByUserAdminPanel(admin.ModelAdmin):
    list_display = ['offer', 'tg_user']


admin.site.register(Offer, OffersAdminPanel)
admin.site.register(TGUser, TGUserAdminPanel)
admin.site.register(DoneOffersByUser, DoneOffersByUserAdminPanel)
