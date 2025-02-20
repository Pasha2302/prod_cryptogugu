from __future__ import annotations

import json
from itertools import chain
from django.core.paginator import Paginator
from django.http import HttpRequest

from app.controllers_views.settings_user import SettingsManager
from app.models_db.banners import ReclamBanner
from app.models_db.coin import Coin

from datetime import timedelta
from django.utils import timezone

from django.db.models import F, Value, Case, When
from django.db.models.functions import Replace, Substr, Cast
from django.db.models import FloatField

now = timezone.now()


class FilterCoin:
    def __init__(self, settings: SettingsManager | None = None, data_coins=None):
        self.settings = settings
        if data_coins is None:
            self.__data_coins = Coin.objects.all()
        else:
            self.__data_coins = data_coins

    def perform_primary_sorting(self):
        if self.settings is not None and self.settings.user_settings_obj:
            if self.settings.user_settings_obj.all_time_best:
                self.__data_coins = self.__data_coins.order_by('-votes')

            elif self.settings.user_settings_obj.today_hot:
                self.__data_coins = self.__data_coins.order_by('-votes24h')

            if self.settings.user_settings_obj.presale:
                self.__data_coins = self.__data_coins.filter(market_cap_presale=True)

            if self.settings.user_settings_obj.audited:
                self.__data_coins = self.__data_coins.filter(labels__name="Audited")

            if self.settings.user_settings_obj.doxxed:
                self.__data_coins = self.__data_coins.filter(labels__name="Doxxed")

            if self.settings.user_settings_obj.new:
                twelve_hours_ago = timezone.now() - timedelta(hours=12)
                self.__data_coins = self.__data_coins.filter(created_at__gte=twelve_hours_ago)

            if (
                    self.settings.user_settings_obj.item_sub_symbol
                    and self.settings.user_settings_obj.item_sub_symbol != 'None'
            ):
                self.__data_coins = self.__data_coins.filter(
                    # Находим записи, где "basic = True"
                    contract_address__basic=True,
                    # Сравниваем slug chain
                    contract_address__chain__slug=self.settings.user_settings_obj.item_sub_symbol
                )

            if self.settings.user_settings_obj.head_filter:
                symbol, sort = self.settings.user_settings_obj.head_filter.split(',')
                if symbol != 'None':
                    self.head_filter_coins(symbol, sort)
            # self.print_time_since_creation()

        else:
            raise TypeError('\nSetting object not found !!!')

    def head_filter_coins(self, symbol: str, sort: str):
        # Сортировка по нескольким полям: order_by('volume', 'id') гарантирует,
        # что если значения volume одинаковы, записи будут отсортированы по id.
        # Это делает порядок сортировки стабильным и однозначным.
        if sort == "DESC":
            self.__data_coins = self.__data_coins.order_by(f'-{symbol}', 'id')
        else:
            self.__data_coins = self.__data_coins.order_by(symbol, 'id')

        if symbol == 'market_cap':
            original_coins = list(self.__data_coins)

            coins_market_cap = [
                coin for coin in original_coins if coin.market_cap is not None
            ]
            coins_market_cap_none = [
                coin for coin in original_coins if (coin.market_cap is None and not coin.market_cap_presale)
            ]
            coins_market_cap_presale = [
                coin for coin in original_coins if (not coin.market_cap and coin.market_cap_presale)
            ]
            self.__data_coins = coins_market_cap + coins_market_cap_presale + coins_market_cap_none

        elif symbol == 'price':
            original_coins = list(self.__data_coins)
            coins_price = [coin for coin in original_coins if coin.price is not None]
            coins_price_none = [coin for coin in original_coins if coin.price is None ]
            self.__data_coins = coins_price + coins_price_none

    def get_coins(self):
        return self.__data_coins

    @staticmethod
    def get_coins_tops_section():
        # top_gainers = Coin.objects.filter(
        #     price_change_percentage__isnull=False
        # ).exclude(price_change_percentage="")[:5]

        # Исключаем нулевые, пустые и нежелательные значения перед выполнением операций
        top_gainers = Coin.objects.filter(
            price_change_percentage__isnull=False,  # Исключаем NULL
        ).exclude(
            price_change_percentage__in=["", "0", "0.0%", "0.00%", "0%", ]  # Исключаем пустые и нулевые значения
        ).annotate(
            price_change_numeric=Case(
                When(
                    price_change_percentage__startswith='asc,',  # Если начинается с 'asc,'
                    then=Cast(
                        Replace(
                            Substr(F('price_change_percentage'), 6, 10),  # Извлекаем часть строки после "asc, "
                            Value('%'),  # Убираем символ процента
                            Value('')
                        ),
                        FloatField()  # Приводим к числовому типу
                    )
                ),
                When(
                    price_change_percentage__startswith='desc,',  # Если начинается с 'desc,'
                    then=-Cast(  # Делаем значение отрицательным
                        Replace(
                            Substr(F('price_change_percentage'), 7, 10),  # Извлекаем часть строки после "desc, "
                            Value('%'),  # Убираем символ процента
                            Value('')
                        ),
                        FloatField()  # Приводим к числовому типу
                    )
                ),
                default=Value(0.0),  # Если формат не подходит, используем 0.0
                output_field=FloatField()
            )
        ).order_by('-price_change_numeric')[:5]  # Сортируем по убыванию и берем топ-5

        return {
            'trending': Coin.objects.order_by('-volume_usd')[:5],
            'most_viewed': Coin.objects.order_by('-views')[:5],
            'top_gainers': top_gainers,
        }

    def print_time_since_creation(self):
        for coin in self.__data_coins:
            time_since_creation = timezone.now() - coin.created_at


class IndexContextManager:
    def __init__(self, request: HttpRequest, slug_chain: str = None):
        self.settings = SettingsManager(request, slug_chain)
        self.customer_data = self.settings.customer_data

        self.current_uri = request.build_absolute_uri()
        self.base_url = self.__get_base_url()

        self.__filter_coin_obj = FilterCoin(self.settings)
        self.__filter_coin_obj.perform_primary_sorting()
        self.__data_coins = self.__filter_coin_obj.get_coins()
        self.__per_page = self.settings.per_page    # __per_page -> Кол-во объектов (монет) в таблице.
        self.__paginator = Paginator(self.__data_coins, self.__per_page)

        # set page_number
        if self.customer_data.get('currentPage') is not None: self.__page_number = self.customer_data['currentPage']
        elif self.customer_data.get('morePage') is not None: self.__page_number = self.customer_data['morePage']
        else: self.__page_number = self.__get_page_number(request)

        if self.__page_number > self.__paginator.num_pages:
            self.__page_number = self.__paginator.num_pages
            self.current_uri = self.base_url + f"/?page={self.__page_number}"

        self.nex_page = self.base_url + f"/?page={self.__page_number + 1}"
        self.prev_page = self.__get_prev_page()

        self.__page_obj = self.__get_page_obj()
        self.__page_start_index = self.get_page_star_index()
        self.__page_end_index = self.get_page_end_index()

        self.top_banners, self.bottom_banners = self.get_reclam_banners()
        self.__context = {
            'user_id': self.settings.user_settings_obj.user_id,
            'top_banners': self.top_banners,
            'bottom_banners': self.bottom_banners,

            'select_number_lines': [10, 20, 50, 100, ],

            'rows_number': self.__per_page,   # __per_page -> Кол-во монет в таблице на странице.
            'page_obj': self.__page_obj,
            'paginator': self.__paginator,

            'page_start_index': self.__page_start_index,
            'page_end_index': self.__page_end_index,

            'page_number': self.__page_number,
            'pagination': self.__calculate_pagination(),
            'page_title': self.__get_page_title(),

            'nex_page': self.nex_page,
            'prev_page': self.prev_page,
            'current_uri': self.current_uri if self.__page_number > 1 else self.base_url,

            'filter_item': self.settings.get_filter_item(),
            'coins_tops_section': self.__filter_coin_obj.get_coins_tops_section()
        }

    def get_page_star_index(self):
        return (self.__page_obj.number - 1) * self.__page_obj.paginator.per_page

    def get_page_end_index(self):
        return self.__page_start_index + len(self.__page_obj.object_list)

    @staticmethod
    def extract_number(banner):
        try:
            # Извлечение числовой части после "banner_"
            return int(banner.position.split('_')[1])
        except (IndexError, ValueError):
            return 0  # Для баннеров, у которых нет числа

    def get_reclam_banners(self):
        top_banners = ReclamBanner.objects.filter(
            position__in=['left-banner', 'right-banner'], is_active=True, start_time__lte=now, end_time__gte=now
        )
        if top_banners:
            top_banners = sorted(top_banners, key=lambda b: b.position == 'left-banner', reverse=True)

        bottom_banners = ReclamBanner.objects.filter(
            position__startswith='banner_', is_active=True, start_time__lte=now, end_time__gte=now
        )
        print("\nbottom banners: ".capitalize(), bottom_banners)
        if bottom_banners:
            bottom_banners = sorted(bottom_banners, key=self.extract_number)

        return top_banners, bottom_banners

    def get_context(self) -> dict:
        return self.__context

    def __get_base_url(self):
        uri = self.current_uri.split('/?')[0]
        if uri.endswith('/'): uri = uri.rstrip('/')
        return uri

    @staticmethod
    def __get_page_number(request):
        page_number = 1
        if request.GET.get('page'):
            page_number = abs(int(request.GET.get('page')))
        if request.POST.get('page'):
            page_number = abs(int(request.POST.get('page')))
        return page_number

    def __get_prev_page(self):
        return self.base_url + f"/?page={self.__page_number - 1}" if self.__page_number >= 2 else None

    def __get_page_obj(self):
        return self.__paginator.get_page(self.__page_number)

    def __get_page_title(self):
        if self.__page_number == 1:
            page_title = "And New Cryptocurrency Listing Portal | CryptoGugu"
        else:
            page_title = f"New Cryptocurrency And DeFi Listing Portal - Page {self.__page_number} | CryptoGugu"
        return page_title

    def __calculate_pagination(self):
        pagination = [1]
        current_page = self.__page_number
        total_pages = self.__paginator.num_pages

        if total_pages < 15: return [p for p in range(1, total_pages + 1)]

        if current_page > 2:
            pagination.extend(
                [p for p in range(current_page - 2, current_page + 3)
                 if 1 < p < total_pages]
            )
        else:
            pagination.extend([p for p in range(current_page, current_page + 3) if p not in [1, total_pages]])

        pagination.append(total_pages)

        average_from_start = ['...', round((pagination[0] + pagination[1]) / 2), '...']
        average_from_end = ['...', round((pagination[-1] + pagination[-2]) / 2), '...']
        if 5 < current_page < (total_pages - 5):
            pagination.insert(1, average_from_start)
            pagination.insert(-1, average_from_end)
            pagination = list(chain.from_iterable(x if isinstance(x, list) else [x] for x in pagination))

        if '...' not in pagination:
            if (pagination[-1] - pagination[-2]) > 4:
                pagination.insert(-1, average_from_end)
                pagination = list(chain.from_iterable(x if isinstance(x, list) else [x] for x in pagination))
            elif total_pages - current_page <= 5:
                pagination.insert(1, average_from_start)
                pagination = list(chain.from_iterable(x if isinstance(x, list) else [x] for x in pagination))

        return pagination


class PromotedCoinsContextManager:
    def __init__(self, request: HttpRequest):
        self.__customer_data = json.loads(request.body).get('data')
        self.__data_head_filter = self.__customer_data.get('active')
        self.args = self.__data_head_filter.split(',')

    def get_filter_item(self):
        filter_item = {
            'head_filter': [
                {'active': False, 'title': 'Market Cap', 'symbol': 'market_cap', 'sort': 'ASC'},
                {'active': False, 'title': 'Price', 'symbol': 'price', 'sort': 'ASC'},
                {'active': False, 'title': 'Volume', 'symbol': 'volume_usd', 'sort': 'ASC'},
                {'active': False, 'title': '24h', 'symbol': 'price_change_24h', 'sort': 'ASC'},
                {'active': False, 'title': 'Launch Date', 'symbol': 'launch_date', 'sort': 'ASC'},
                {'active': False, 'title': 'Votes', 'symbol': 'votes', 'sort': 'ASC'},
                {'active': False, 'title': 'Votes 24', 'symbol': 'votes24h', 'sort': 'ASC'},
            ],
        }

        if self.args:
            for head_filter in filter_item['head_filter']:
                symbol, sort = self.args[0], self.args[1]
                if head_filter['symbol'] == symbol:
                    head_filter['sort'] = sort
                    head_filter['active'] = True
                    break

        return filter_item

    def get_context(self):
        data_coins = Coin.objects.filter(promoted__isnull=False).select_related('promoted')
        if not data_coins:
            return None

        filter_coins_obj = FilterCoin(data_coins=data_coins)
        filter_coins_obj.head_filter_coins(symbol=self.args[0], sort=self.args[1])
        object_list = filter_coins_obj.get_coins()
        return {
            'filter_item': self.get_filter_item(),
            'page_obj': {'object_list': object_list},
            'page_start_index': 0,
        }


class VoteManager:
    def __init__(self, request: HttpRequest):
        self.__settings = SettingsManager(request)
        self.__data_vote = None

    def get_data_vote(self):
        return self.__data_vote

    def check_and_save_vote(self):
        if self.__settings.status_votes.get("status") == "Vote registered":
            self.__data_vote = self.save_vote(self.__settings.status_votes['vole_coin_id'])
        else:
            self.__data_vote = self.__settings.status_votes

    @staticmethod
    def save_vote(vole_coin_id):
        # Увеличьте количество голосов для указанной монеты
        coin = Coin.objects.get(id=vole_coin_id)
        coin.votes += 1
        coin.votes24h += 1
        coin.save()
        return {"daily_vote": coin.votes24h, "vote": coin.votes}



