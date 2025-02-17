from django.db import models


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

    class Meta:
        ordering = ["id"]
        verbose_name = "Airdrops"
        verbose_name_plural = "Airdrops"

    def __str__(self):
        return self.name

