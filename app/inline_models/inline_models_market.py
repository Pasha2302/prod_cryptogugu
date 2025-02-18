from django.contrib import admin

from app.models_db.coin import Market


class MarketInline(admin.StackedInline):
    model = Market
    extra = 1
