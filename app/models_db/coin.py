from django.db import models
from django.utils import timezone

from app.models_db.functions.functions_for_coins import normalized_price_coin, get_price_change
from app.models_db.secondary import save_slug


class PromotedCoin(models.Model):
    """
    Модель для хранения информации о продвигаемых монетах.
    """
    coin = models.OneToOneField("Coin", on_delete=models.CASCADE, related_name='promoted')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()

    class Meta:
        ordering = ["id"]
        verbose_name = "Promoted Coin"
        verbose_name_plural = "Promoted Coin"

    def __str__(self):
        return f"Promoted: {self.coin.name} from {self.start_date} to {self.end_date}"


class AbstractCoin(models.Model):
    """
    Абстрактная модель для хранения общих полей монет.
    """
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True, null=True)
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=50)

    market_cap = models.DecimalField(max_digits=35, decimal_places=2, blank=True, null=True)

    price = models.DecimalField(max_digits=64, decimal_places=18, blank=True, null=True)  # Уменьшена точность
    format_price = models.CharField(max_length=64, blank=True, null=True)

    liquidity_usd = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    volume_usd = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    volume_btc = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    price_change_24h = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Price Change 24h", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")

    # Поле для счётчика просмотров
    views = models.PositiveIntegerField(default=0)
    # Поле для хранения процентного изменения цены
    price_change_percentage = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        get_price_change(self)
        normalized_price_coin(self)
        save_slug(self, super(), additionally=None, *args, **kwargs)

    def __str__(self):
        return self.name

# ================================================== Info =========================================================== #


class AuditInfo(models.Model):
    coin = models.OneToOneField('Coin', on_delete=models.CASCADE, related_name="audit_info")

    audit_company = models.CharField(max_length=255, blank=True, null=True)
    audit_link = models.URLField(blank=True, null=True)
    doxxed = models.URLField(blank=True, null=True)


class TaxInfo(models.Model):
    coin = models.OneToOneField('Coin', on_delete=models.CASCADE, related_name="tax_info")

    sell_tax = models.IntegerField(default=0, blank=True, null=True)
    buy_tax = models.IntegerField(default=0, blank=True, null=True)
    slippage = models.IntegerField(default=0, blank=True, null=True)

# ------------------------------------------------------------------------------------------------------------ #


class PresaleInfo(models.Model):
    coin = models.OneToOneField('Coin', on_delete=models.CASCADE, related_name="presale_info")
    presale = models.BooleanField(default=False)

    softcap = models.CharField(max_length=50, blank=True, null=True)
    presale_link = models.URLField(blank=True, null=True)
    hardcap = models.CharField(max_length=50, blank=True, null=True)
    presale_date = models.DateField(blank=True, null=True)
    whitelist = models.BooleanField(default=False)


class CoinDescription(models.Model):
    coin = models.OneToOneField('Coin', on_delete=models.CASCADE, related_name="description")

    desc_0 = models.TextField(blank=True, null=True)
    desc_1 = models.TextField(blank=True, null=True)
    desc_2 = models.TextField(blank=True, null=True)
    desc_3 = models.TextField(blank=True, null=True)
    desc_4 = models.TextField(blank=True, null=True)
    desc_5 = models.TextField(blank=True, null=True)


class CoinSocials(models.Model):
    coin = models.ForeignKey('Coin', on_delete=models.CASCADE, related_name="socials")

    name = models.CharField(max_length=50, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    icon = models.ImageField(upload_to='social_icons/', max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)


# =================================================================================================================== #


class ContractAddress(models.Model):
    coin = models.ForeignKey(
        'Coin',
        on_delete=models.SET_NULL,
        related_name="contract_address",
        null=True,
    )
    chain = models.ForeignKey(
        'Chain',
        on_delete=models.SET_NULL,
        related_name="contract_address",
        null=True,
    )
    contract_address = models.CharField(max_length=52, blank=True, null=True)
    basic = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]
        verbose_name = "Contract Address"
        verbose_name_plural = "Contract Addresses"

    def __str__(self):
        _str = 'Contract Address [Not Assigned]'
        if self.coin and self.chain:
            _str = f"Contract Address [{self.coin.name}] [{self.chain.name}]"
        return _str

    def save(self, *args, **kwargs):
        # Если первая запись, устанавливаем basic=True
        if self.coin and not ContractAddress.objects.filter(coin=self.coin).exists():
            self.basic = True
        elif self.basic:
            # Если вручную установлено basic=True, сбрасываем у других
            ContractAddress.objects.filter(coin=self.coin, basic=True).update(basic=False)

        super().save(*args, **kwargs)  # Сохраняем объект


class Chain(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=50, blank=True, null=True)
    path_chain_img = models.FileField(upload_to='chain_images/', max_length=255, blank=True, null=True)

    class Meta:
        ordering = ["id"]

    def save(self, *args, **kwargs):
        save_slug(self, super(), additionally=None, *args, **kwargs)

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name

# ================================================== Coin =========================================================== #


class Coin(AbstractCoin):
    """
    Модель для хранения информации о монетах.
    """

    selected_auto_voting = models.BooleanField(default=False)
    labels = models.ManyToManyField('Label', related_name='coin', blank=True, )

    votes = models.IntegerField(default=0)
    votes24h = models.IntegerField(default=0)
    market_cap_presale = models.BooleanField(default=False)
    path_coin_img = models.ImageField(upload_to='coin_images/', max_length=255, blank=True, null=True)

    launch_date = models.DateField(blank=True, null=True)

    objects = models.Manager()

    class Meta:
        ordering = ["id"]
        verbose_name = "Coin"
        verbose_name_plural = "Coins"

    def get_contract_address_basic(self):
        """
        Возвращает единственный объект contract_address, где basic=True,
        или None, если такой записи нет.
        """
        return self.contract_address.filter(basic=True).first()

    def get_all_contract_addresses(self):
        """
        Возвращает все связанные contract_address.
        """
        return self.contract_address.all()

    def get_chain_from_basic_contract(self):
        """
        Возвращает объект chain из записи contract_address, где basic=True.
        Если таких записей нет, возвращает None.
        """
        basic_contract = self.get_contract_address_basic()
        return basic_contract.chain if basic_contract else None

    def get_global_rank(self):
        # Рейтинг по количеству голосов "votes" за все время
        return Coin.objects.filter(votes__gt=self.votes).count() + 1

    def get_daily_rank(self):
        # Рейтинг по количеству голосов "votes24h" за 24 часа
        return Coin.objects.filter(votes24h__gt=self.votes24h).count() + 1

# ------------------------------------------------------------------------------------------------------------- #


class BaseCoin(AbstractCoin):
    """
    Модель для хранения базовой информации о монетах.
    """
    contract_address = models.CharField(max_length=52, blank=True, null=True)
    pair_url = models.URLField(max_length=500, blank=True, null=True)
    path_coin_img = models.ImageField(upload_to='base_coin_images/', max_length=255, blank=True, null=True)

    name_chain = models.CharField(max_length=50, default='', blank=True, )
    symbol_chain = models.CharField(max_length=50, default='', blank=True, )
    path_chain_img = models.ImageField(upload_to='chain_images/', max_length=255, blank=True, null=True)

    objects = models.Manager()

    class Meta:
        ordering = ["id"]
        verbose_name = "Base Coin"
        verbose_name_plural = "Base Coins"

