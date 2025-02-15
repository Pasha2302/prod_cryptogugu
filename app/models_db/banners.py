from django.db import models
from django.utils import timezone


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