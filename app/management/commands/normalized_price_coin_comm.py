from django.core.management.base import BaseCommand

from app.models_db.coin import Coin
from app.models_db.functions.functions_for_coins import normalized_price_coin


class Command(BaseCommand):
    help = "Добавляет форматированную цену монете"

    def handle(self, *args, **kwargs):
        for coin in Coin.objects.all():
            normalized_price_coin(coin=coin)
            coin.save()


# python manage.py normalized_price_coin_comm
