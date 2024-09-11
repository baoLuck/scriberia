from django.db import models


class Offer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    reward = models.DecimalField(default=0.1, decimal_places=4, max_digits=10)
    link = models.CharField(max_length=100, default='https://t.me/yakrutkaneki')
    available = models.BooleanField(default=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TGUser(models.Model):
    tg_id = models.IntegerField(unique=True)
    chat_id = models.IntegerField(unique=True)
    tg_username = models.CharField(max_length=255)
    ton_balance = models.DecimalField(default=0.0, decimal_places=4, max_digits=10)
    scribe_balance = models.IntegerField(default=0)
    creation_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    done_tasks = models.ManyToManyField('Offer', blank=True, related_name='users', through='DoneOffersByUser')

    def __str__(self):
        return self.tg_username


class DoneOffersByUser(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    tg_user = models.ForeignKey(TGUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)


