from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import uuid
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError


def save_slug(self, _super, additionally=None, *args, **kwargs):
    if additionally is None: additionally = ''
    if not self.slug: self.slug = slugify(f"{self.name} {additionally}".strip())
    _super.save(*args, **kwargs)


class SiteSettings(models.Model):
    """
    Модель для хранения настроек сайта. Разрешена только одна запись.
    """
    count_coins = models.IntegerField(null=True, blank=True)
    count_airdrops = models.IntegerField(null=True, blank=True)

    objects = models.Manager()  # Используем стандартный менеджер

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError('Можно создать только одну запись Site Settings')
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return "Site Data"


class ReclamBannerPopUp(models.Model):
    """
    Модель для хранения баннеров с возможностью смены изображений.
    """
    BANNER_POSITIONS = [
        ('rb', 'Right Banner'),
        ('cb', 'Center Banner'),
        ('lb', 'Left Banner'),
    ]

    position = models.CharField(
        max_length=2,
        choices=BANNER_POSITIONS,
        default='rb',
        verbose_name="Banner position"
    )
    link = models.URLField(blank=True, null=True)
    images = models.ManyToManyField(
        'BannerImagePopUp',
        related_name='banners',
        verbose_name="Banner images"
    )
    start_time = models.DateTimeField(verbose_name="Image display start time")
    end_time = models.DateTimeField(verbose_name="Image display end time")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    current_image = models.ForeignKey(
        'BannerImagePopUp',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="current_banner",
        verbose_name="Current Image"
    )

    class Meta:
        verbose_name = "Reclam Banner PopUp"
        verbose_name_plural = "Reclam Banners PopUps"

    def __str__(self):
        return f"Banner PopUp ({self.get_position_display()})"

    def get_current_image(self):
        """Возвращает текущую картинку на основе установленного времени."""
        if self.images.exists():
            now_time = timezone.now()
            if self.start_time <= now_time <= self.end_time:
                elapsed_time = (now_time - self.start_time).total_seconds()
                total_images = self.images.count()
                index = int(elapsed_time // 3600) % total_images  # Меняется каждый час
                return self.images.all()[index]
        return None


class BannerImagePopUp(models.Model):
    """
    Модель для хранения изображений баннеров.
    """
    image = models.ImageField(upload_to="banners_pop_ups/", verbose_name="Изображение")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Загружено")

    def __str__(self):
        return f"Banner Image ({self.uploaded_at})"


class ReclamBanner(models.Model):
    """
    Модель для хранения рекламных баннеров.
    """
    POSITION_CHOICES = [
        ('right-banner', 'Top Right Banner'),
        ('left-banner', 'Top Left Banner'),
        ('banner_1', 'Banner Bottom 1'),
        ('banner_2', 'Banner Bottom 2'),
        ('banner_3', 'Banner Bottom 3'),
        ('banner_4', 'Banner Bottom 4'),
        ('banner_5', 'Banner Bottom 5'),
        ('banner_6', 'Banner Bottom 6'),
    ]

    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Reclam Banner'
        verbose_name_plural = 'Reclam Banners'
        indexes = [
            models.Index(fields=['start_time', 'end_time']),  # Индекс для оптимизации
        ]

    def is_currently_active(self):
        """Проверяет, активен ли баннер в текущий момент времени."""
        now = timezone.now()
        return self.is_active and self.start_time <= now <= self.end_time

    def __str__(self):
        return f"{self.position} banner"


class UserSettingsManager(models.Manager):
    """
    Кастомный менеджер для модели UserSettings.
    """
    def get_or_create_default_settings(self, user_id=None):
        """
        Создает или возвращает настройки для пользователя.
        Если user_id не указан, используется дефолтный ID.
        """
        if user_id is None: user_id = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")

        settings, created = self.get_or_create(user_id=user_id)
        return settings


class UserSettings(models.Model):
    """
    Модель для хранения пользовательских настроек.
    """
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    per_page = models.PositiveIntegerField(default=10)
    theme_site = models.CharField(max_length=10, default='dark')

    today_hot = models.BooleanField(default=False)
    all_time_best = models.BooleanField(default=True)
    gem_pad = models.BooleanField(default=False)
    new = models.BooleanField(default=False)
    presale = models.BooleanField(default=False)
    doxxed = models.BooleanField(default=False)
    audited = models.BooleanField(default=False)

    item_sub_symbol = models.CharField(max_length=20, null=True)
    head_filter = models.CharField(max_length=30, null=True)
    coins_votes = ArrayField(models.CharField(max_length=50), verbose_name="Coins Votes", blank=True, default=list)

    objects = UserSettingsManager()

    def __str__(self):
        return f"Settings for user {self.user_id}"

    def has_voted_for(self, coin_id):
        """Проверяет, голосовал ли пользователь за монету."""
        return coin_id in self.coins_votes

    def vote_for_coin(self, coin_id):
        """Добавляет голос за монету."""
        if not self.has_voted_for(coin_id):
            self.coins_votes.append(coin_id)
            self.save()
            return True
        return False


class Airdrops(models.Model):
    """
    Модель для хранения информации о аирдропах.
    """
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    end_date = models.DateField(blank=True, null=True)
    reward = models.CharField(max_length=255)
    path_airdrop_img = models.ImageField(upload_to='airdrop_images/', max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")
    objects = models.Manager()

    def __str__(self):
        return self.name

#


class PromotedCoins(models.Model):
    """
    Модель для хранения информации о продвигаемых монетах.
    """
    coin = models.OneToOneField("Coin", on_delete=models.CASCADE, related_name='promoted')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Promoted: {self.coin.name} from {self.start_date} to {self.end_date}"


class AbstractCoin(models.Model):
    """
    Абстрактная модель для хранения общих полей монет.
    """
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True, null=True)

    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=50)
    contract_address = models.CharField(max_length=52, blank=True, null=True)
    market_cap = models.DecimalField(max_digits=35, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=64, decimal_places=18, blank=True, null=True)  # Уменьшена точность
    liquidity_usd = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    volume_usd = models.DecimalField(max_digits=20, decimal_places=2)
    volume_btc = models.DecimalField(max_digits=20, decimal_places=2)
    price_change_24h = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price Change 24h")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")

    # Поле для счётчика просмотров
    views = models.PositiveIntegerField(default=0)
    # Поле для хранения процентного изменения цены
    price_change_percentage = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__get_price_change()
        save_slug(self, super(), additionally=None, *args, **kwargs)

    def __get_price_change(self):
        if self.pk is not None:
            old = self.__class__.objects.filter(pk=self.pk).first()
            if old is not None and old.price is not None and self.price is not None:
                try:
                    old_price = Decimal(old.price)  # Приводим к Decimal
                    new_price = Decimal(self.price)  # Приводим к Decimal

                    if old_price == 0:
                        self.price_change_percentage = None
                    else:
                        change = (new_price - old_price) / old_price * 100
                        direction = "asc" if change >= 0 else "desc"
                        self.price_change_percentage = f"{direction}, {abs(change):.2f}%"
                except (InvalidOperation, ZeroDivisionError, ValueError):
                    self.price_change_percentage = None
            else:
                self.price_change_percentage = None
        else:
            self.price_change_percentage = None

    @staticmethod
    def format_decimal_number(number: Decimal) -> str:
        """
        Форматирует десятичное число для отображения.
        Убирает лишние нули и округляет до 2 знаков после запятой.
        """
        if number is None:
            return "0"

        number_str = format(number, 'f').rstrip('0')
        if '.' in number_str:
            integer_part, fractional_part = number_str.split('.')
            if not fractional_part or int(fractional_part) == 0:
                return integer_part if integer_part else "0"

            first_non_zero_idx = len(fractional_part) - len(fractional_part.lstrip('0'))
            zero_count = first_non_zero_idx

            if zero_count > 3:
                significant_part = fractional_part[first_non_zero_idx: first_non_zero_idx + 2]
                return f"0.|{zero_count}|{significant_part}"
            else:
                return str(round(float(number_str), 2))
        else:
            return number_str

    @property
    def normalized_price(self):
        """Возвращает нормализованную цену."""
        if self.price is not None:
            return self.format_decimal_number(self.price.normalize())
        return None

    def __str__(self):
        return self.name


class Coin(AbstractCoin):
    """
    Модель для хранения информации о монетах.
    """
    selected_auto_voting = models.BooleanField(default=False)
    tags = ArrayField(models.CharField(max_length=50), verbose_name="Tags", blank=True, default=list)
    chain = models.CharField(max_length=30)
    votes = models.IntegerField(default=0)
    votes24h = models.IntegerField(default=0)
    market_cap_presale = models.BooleanField(default=False)

    path_coin_img = models.ImageField(upload_to='coin_images/', max_length=255)
    path_chain_img = models.ImageField(upload_to='chain_images/', max_length=255)

    launch_date_str = models.CharField(max_length=50, blank=True, null=True)
    launch_date = models.DateField(blank=True, null=True)

    objects = models.Manager()

    class Meta:
        ordering = ["id"]
        verbose_name = "Coin"
        verbose_name_plural = "Coins"


class BaseCoin(AbstractCoin):
    """
    Модель для хранения базовой информации о монетах.
    """
    pair_url = models.URLField(max_length=200)
    path_coin_img = models.ImageField(upload_to='base_coin_images/', max_length=255)
    path_chain_img = models.ImageField(upload_to='chain_images/', max_length=255)

    objects = models.Manager()

    class Meta:
        ordering = ["id"]
        verbose_name = "Base Coin"
        verbose_name_plural = "Base Coins"

