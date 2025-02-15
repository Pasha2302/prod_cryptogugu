import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.exceptions import ValidationError


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

# ================================================================================================================ #


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

