from django.contrib import admin
from django.utils.html import mark_safe

from app.admin_forms.coin_form import CoinAdminForm
from app.inline_models.inline_models_coin import ContractAddressInline, AuditInfoInline, TaxInfoInline, \
    PresaleInfoInline, CoinDescriptionInline, CoinSocialsInline
from app.inline_models.inline_models_market import MarketInline
from app.models_db.coin import Coin, Market, ChainMarket


# @admin.register(Market)
# class MarketAdmin(admin.ModelAdmin):
#     pass


@admin.register(ChainMarket)
class ChainMarketAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('id', 'chain')
    autocomplete_fields = ('chain', )

    inlines = (MarketInline, )


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    change_form_template = 'app/admin/coin_change_form.html'
    form = CoinAdminForm
    readonly_fields = ('slug', 'price_change_percentage', 'format_price', )
    list_display = ('id', 'display_coin_image', 'name', 'symbol', 'format_price')
    list_display_links = ('name', 'symbol',)
    search_fields = ('name', )

    inlines = (
        ContractAddressInline, AuditInfoInline, TaxInfoInline,
        PresaleInfoInline, CoinDescriptionInline, CoinSocialsInline
    )
    filter_horizontal = ('labels', )

    def display_coin_image(self, obj):
        if obj.path_coin_img:
            return mark_safe(f'<img src="{obj.path_coin_img.url}" style="width: 50px; height: 50px;" />')
        return "No Image"
    display_coin_image.short_description = 'Coin Image'


