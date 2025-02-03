from django.core.management.base import BaseCommand
from django.utils.text import slugify

from app.models import Coin, BaseCoin


class Command(BaseCommand):
    help = 'Генерирует slug для монет на основе их имени'

    def handle(self, *args, **options):
        # Обрабатываем объекты модели Coin
        coins = Coin.objects.all()
        for coin in coins:
            # Если slug пустой или не установлен, генерируем его
            if not coin.slug:
                coin.slug = slugify(coin.name)
                coin.save(update_fields=['slug'])
                self.stdout.write(self.style.SUCCESS(
                    f'Coin "{coin.name}" обновлён, slug: {coin.slug}'
                ))
            else:
                self.stdout.write(
                    f'Coin "{coin.name}" уже имеет slug: {coin.slug}'
                )

        # Если необходимо, можно сделать то же самое для BaseCoin:
        base_coins = BaseCoin.objects.all()
        for coin in base_coins:
            if not coin.slug:
                coin.slug = slugify(coin.name)
                coin.save(update_fields=['slug'])
                self.stdout.write(self.style.SUCCESS(
                    f'BaseCoin "{coin.name}" обновлён, slug: {coin.slug}'
                ))
            else:
                self.stdout.write(
                    f'BaseCoin "{coin.name}" уже имеет slug: {coin.slug}'
                )

        self.stdout.write(self.style.SUCCESS('Генерация slug завершена.'))


# python manage.py generate_slug

# Запуск в фоне с выводом в File output.log:
# nohup python manage.py generate_slug > output.log 2>&1 &

# Проверка работы процесса:
# ps aux | grep generate_slug
