from django.utils.translation import gettext as _

from app.models import BaseCoin, Airdrops, Coin, SiteSettings, ReclamBannerPopUp
from django.http import HttpRequest


class BaseContextManager:
    def __init__(self, request: HttpRequest):
        self.user_id_str = request.COOKIES.get('userId')

        self.site_settings: SiteSettings = SiteSettings.objects.first()
        self.base_coins = BaseCoin.objects.all()
        print('\nSite Settings Obj:', self.site_settings)

        if self.site_settings and self.site_settings.count_coins:
            self.count_coins = self.site_settings.count_coins
        else:
            self.count_coins = Coin.objects.count()

        if self.site_settings and self.site_settings.count_airdrops:
            self.count_airdrops = self.site_settings.count_airdrops
        else:
            self.count_airdrops = Airdrops.objects.count()

    def get_context(self):
        banners = tuple()
        if not self.user_id_str:
            banners = ReclamBannerPopUp.objects.filter(is_active=True)
            for banner in banners:
                banner.current_image = banner.get_current_image()  # Устанавливаем текущую картинку
        print(f"\n[ReclamBannerPopUp]\nNew Usr id: {self.user_id_str}\nBanners: {banners}")

        return {
            'banners_pop_ups': banners,

            'top_rate_items': {
                'base_coins_list': self.base_coins,
                'count_coins_int': self.count_coins,
                'count_airdrops_int': self.count_airdrops,
            },

            'menu_items': [
                {'name': _('Coin Ranking'), 'url': 'index'},
                {'name': _('Airdrops'), 'url': 'airdrops'},
                {'name': _('Promotion'), 'url': 'promote'},

                {'name': _('Careers'), 'url': 'careers'},
                {'name': _('Our Partners'), 'url': 'partners'},
                {'name': _('Contact us'), 'url': 'contact'},

                {'name': _('Games'), 'url': '#'},
                {'name': _('Free Signals'), 'url': '#'},
                {'name': _('About Us'), 'url': '#'},
                {'name': _('Blog'), 'url': 'blog'},
            ],

        }

