from django.http import HttpRequest, Http404

from django.db import transaction
from django.db.models import F

from app.controllers_views.base import BaseContextManager
from app.models_db.coin import Coin


class CoinPageContextManager:

    def __init__(self, request: HttpRequest, chain_slug: str, coin_slug: str):
        self.request = request
        self.chain_slug = chain_slug
        self.coin_slug = coin_slug

    def get_coin_and_add_views(self):
        with transaction.atomic():
            # Используем связь contract_address для фильтрации по chain_slug
            Coin.objects.filter(
                contract_address__chain__slug=self.chain_slug,  # Правильное использование related_name
                slug=self.coin_slug
            ).update(views=F('views') + 1)

            try:
                # Получаем монету с обновленным счетчиком просмотров
                return Coin.objects.get(
                    contract_address__chain__slug=self.chain_slug,  # Используем related_name
                    slug=self.coin_slug
                )
            except Coin.DoesNotExist:
                # Если монета не найдена, возвращаем 404
                raise Http404

    def get_context(self):
        context: dict = BaseContextManager(self.request).get_context()
        context['coin'] = self.get_coin_and_add_views()
        return context

