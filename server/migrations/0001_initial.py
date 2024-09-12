# Generated by Django 5.1 on 2024-09-02 13:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Offer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                (
                    "reward",
                    models.DecimalField(decimal_places=4, default=0.1, max_digits=10),
                ),
                (
                    "link",
                    models.CharField(
                        default="https://t.me/yakrutkaneki",
                        max_length=100,
                    ),
                ),
                ("available", models.BooleanField(default=True)),
                ("creation_time", models.DateTimeField(auto_now_add=True)),
                ("update_time", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="DoneOffersByUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "offer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="server.offer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TGUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tg_id", models.IntegerField(unique=True)),
                ("chat_id", models.IntegerField(unique=True)),
                ("tg_username", models.CharField(max_length=255)),
                (
                    "ton_balance",
                    models.DecimalField(decimal_places=4, default=0.0, max_digits=10),
                ),
                ("scribe_balance", models.IntegerField(default=0)),
                ("creation_time", models.DateTimeField(auto_now_add=True)),
                ("update_time", models.DateTimeField(auto_now=True)),
                (
                    "done_tasks",
                    models.ManyToManyField(
                        blank=True,
                        related_name="users",
                        through="server.DoneOffersByUser",
                        to="server.offer",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="doneoffersbyuser",
            name="tg_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="server.tguser",
            ),
        ),
    ]
