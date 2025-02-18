from django.http import HttpRequest, Http404

from django.db import transaction
from django.db.models import F

from app.controllers_views.base import BaseContextManager
from app.models_db.coin import Coin, Market


class CoinPageContextManager:

    def __init__(self, request: HttpRequest, chain_slug: str, coin_slug: str):
        self.request = request
        self.chain_slug = chain_slug
        self.coin_slug = coin_slug

    def get_coin_and_add_views(self) -> Coin:
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
        coin = self.get_coin_and_add_views()
        contracts_addresses = coin.get_all_contract_addresses()
        base_address = contracts_addresses.filter(basic=True).first()

        # Получение всех описаний из CoinDescription, которые не являются пустыми
        if hasattr(coin, 'description'):  # Проверяем, есть ли описание у монеты
            descriptions = [
                getattr(coin.description, f"desc_{i}")
                for i in range(6)  # desc_0 - desc_5
                if getattr(coin.description, f"desc_{i}", None)  # Описание не пустое
            ]
        else:
            descriptions = []

        # Базовый чейн монеты
        basic_chain = coin.get_chain_from_basic_contract()

        # Получение всех маркетов для базового чейна
        if basic_chain and base_address:
            markets = Market.objects.filter(market__chain=basic_chain)
            market_links = [
                {
                    "market_name": market.name_market,
                    "url": market.build_url(base_address.contract_address),
                    "image": market.image.url if market.image else None
                }
                for market in markets
            ]
        else:
            market_links = []

        context['obj_coin'] = coin
        context['obj_basic_chain'] = basic_chain
        context['contracts_addresses'] = contracts_addresses
        context['base_address'] = base_address or {}
        context['obj_socials'] = coin.socials.all()

        context['more_coins'] = Coin.objects.filter(contract_address__chain__slug=self.chain_slug)
        context['descriptions'] = descriptions  # Добавляем в контекст непустые описания

        # Добавляем список маркетов в контекст
        context['markets'] = market_links

        return context




