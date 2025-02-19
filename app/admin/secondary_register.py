from django.contrib import admin

from app.admin_forms.chain_form import ChainAdminForm
from app.admin_forms.coin_form import BaseCoinAdminForm
from app.admin_forms.promoted_coins_form import PromotedCoinsForm
from app.models_db.airdrops import Airdrops
from app.models_db.banners import ReclamBannerPopUp, BannerImagePopUp, ReclamBanner
from app.models_db.coin import PromotedCoin, ContractAddress, Chain, BaseCoin, Label
from app.models_db.settings import SiteSettings

from django.utils.timezone import localtime


@admin.register(PromotedCoin)
class PromotedCoinsAdmin(admin.ModelAdmin):
    """
    Атрибуты:
        form (PromotedCoinsForm): настраиваемая форма, используемая для ввода данных в админке.
        list_display (кортеж): поля, отображаемые в представлении списка в интерфейсе администратора.
        list_filter (кортеж): фильтруемые поля в представлении списка администратора для целевого поиска.
        search_fields (кортеж): поля для поиска в интерфейсе администратора.

    Методы:
        get_queryset(request):
        возвращает оптимизированный набор запросов с предварительно загруженной связанной информацией о монетах.
    """
    form = PromotedCoinsForm
    list_display = ('coin', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('coin__name', 'coin__symbol')
    autocomplete_fields = ('coin',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('coin')

    # def formatted_start_date(self, obj):
    #     """Форматирует дату начала в 24-часовом формате UTC."""
    #     return localtime(obj.start_date).strftime('%Y-%m-%d %H:%M:%S')  # Формат UTC
    #
    # formatted_start_date.admin_order_field = 'start_date'  # Позволяет сортировать по оригинальному полю
    # formatted_start_date.short_description = 'Start Date (UTC)'  # Название колонки в интерфейсе
    #
    # def formatted_end_date(self, obj):
    #     """Форматирует дату окончания в 24-часовом формате UTC."""
    #     return localtime(obj.end_date).strftime('%Y-%m-%d %H:%M:%S')  # Формат UTC
    #
    # formatted_end_date.admin_order_field = 'end_date'
    # formatted_end_date.short_description = 'End Date (UTC)'


# ================================================================================================================== #

@admin.register(ReclamBannerPopUp)
class ReclamBannerPopUpsAdmin(admin.ModelAdmin):
    list_display = ['position', 'is_active', 'start_time', 'end_time']
    list_filter = ['position', 'is_active']
    search_fields = ['position', 'link']
    filter_horizontal = ['images']


@admin.register(BannerImagePopUp)
class BannerImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'uploaded_at']
    search_fields = ['id']


# ==================================================================================================================


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Разрешить добавление записи только если её еще нет
        if SiteSettings.objects.exists():
            return False
        return super(SiteSettingsAdmin, self).has_add_permission(request)


@admin.register(ReclamBanner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('position', 'start_time', 'end_time', 'is_active', 'is_currently_active')
    list_filter = ('position', 'is_active', 'start_time', 'end_time')
    search_fields = ('position',)

# ================================================================================================================== #


# @admin.register(ContractAddress)
# class ContractAddressAdmin(admin.ModelAdmin):
#     pass


@admin.register(Chain)
class ChainAdmin(admin.ModelAdmin):
    form = ChainAdminForm
    readonly_fields = ('slug', )
    search_fields = ('name', )


@admin.register(Airdrops)
class AirdropsAdmin(admin.ModelAdmin):
    pass


@admin.register(BaseCoin)
class BaseCoinAdmin(admin.ModelAdmin):
    form = BaseCoinAdminForm


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    pass
