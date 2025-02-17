from django.contrib import admin

from app.models_db.coin import (
    ContractAddress, AuditInfo, TaxInfo, PresaleInfo, CoinDescription, CoinSocials
)


class ContractAddressInline(admin.TabularInline):
    model = ContractAddress
    extra = 1
    fk_name = 'coin'  # Указываем, к какой ForeignKey привязана Inline-модель
    readonly_fields = ('basic', )

    can_delete = True
    fields = ('contract_address', 'chain', 'basic', )
    autocomplete_fields = ('chain', )


class AuditInfoInline(admin.StackedInline):
    model = AuditInfo
    extra = 0
    min_num = 1


class TaxInfoInline(admin.StackedInline):
    model = TaxInfo
    extra = 0
    min_num = 1


class PresaleInfoInline(admin.StackedInline):
    model = PresaleInfo
    extra = 0
    min_num = 1


class CoinDescriptionInline(admin.StackedInline):
    model = CoinDescription
    extra = 0
    min_num = 1


class CoinSocialsInline(admin.TabularInline):
    model = CoinSocials
    extra = 1
