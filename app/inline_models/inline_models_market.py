from django.contrib import admin

from app.admin_forms.market_admin_form import MarketAdminForm
from app.models_db.coin import Market


class MarketInline(admin.StackedInline):
    model = Market
    form = MarketAdminForm
    extra = 1
