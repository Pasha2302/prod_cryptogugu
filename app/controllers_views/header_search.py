import json

from django.db.models import Q
from django.http import HttpRequest

from app.models_db.airdrops import Airdrops
from app.models_db.coin import Coin


class HeaderSearchManager:
    def __init__(self, request: HttpRequest):
        self.__customer_data: dict = json.loads(request.body).get('data')
        self.__context = self.search()
        print(f"\nHeader Search Manager [data]: {self.__customer_data}")

    def search(self):
        if self.__customer_data.get('query'):
            query = self.__customer_data['query']

            # Поиск в модели Coin
            coin_results = Coin.objects.filter(
                Q(name__icontains=query) | Q(symbol__icontains=query) |
                Q(contract_address__contract_address__icontains=query)
            ).distinct()

            # Поиск в модели Airdrops
            airdrop_results = Airdrops.objects.filter(name__icontains=query)

            return coin_results, airdrop_results
        else:
            return [], []

    def get_context(self):
        coin_results, airdrop_results = self.__context

        coins = [
            {
                'name': coin.name,
                'slug': coin.slug,
                'symbol': coin.symbol,
                'contract_address': coin.get_contract_address_basic().contract_address
                if coin.get_contract_address_basic() else None,
                'chain': coin.get_chain_from_basic_contract()
                if coin.get_chain_from_basic_contract() else None,
                'img_path': f'{coin.path_coin_img.url}' if coin.path_coin_img else None
            } for coin in coin_results
        ]

        airdrops = [
            {
                'name': airdrop.name,
                'status': airdrop.status,
                'end_date': airdrop.end_date,
                'reward': airdrop.reward,
                'img_path': f'{airdrop.path_airdrop_img.url}' if airdrop.path_airdrop_img else None
            } for airdrop in airdrop_results
        ]

        return {
            'coins': coins,
            'airdrops': airdrops,
            'count_coins': len(coins),
            'count_airdrops': len(airdrops)
        }
