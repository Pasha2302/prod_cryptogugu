import os
from django.conf import settings


from django.core.management.base import BaseCommand
from random import randint, uniform, choice, sample
from faker import Faker

from app.models_db.coin import Label, Chain, AuditInfo, PresaleInfo, TaxInfo, CoinDescription, CoinSocials, \
    ContractAddress, Coin

fake = Faker()


class Command(BaseCommand):
    help = "Создает указанное количество фейковых монет и связанные с ними данные"

    def add_arguments(self, parser):
        parser.add_argument(
            'amount',
            type=int,
            help="Количество фейковых монет для создания",
        )

    @staticmethod
    def get_random_image_from_directory(directory):
        """
        Возвращает случайный путь к изображению из указанной директории.
        """
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if not files:
            return None  # Если папка пуста, возвращаем None
        return os.path.join('coin_images', files.pop(randint(0, len(files) - 1)))

    def handle(self, *args, **kwargs):
        amount = kwargs['amount']

        # Генерация Labels и Chains
        labels = [
            Label.objects.get_or_create(name='Audited')[0],
            Label.objects.get_or_create(name='Doxxed')[0],
        ]

        chains = list(Chain.objects.all())

        coin_images_dir = os.path.join(settings.BASE_DIR, 'media', 'coin_images')

        for _ in range(amount):
            # Получаем случайное изображение
            random_image = self.get_random_image_from_directory(coin_images_dir)

            # Создаем монету
            coin = Coin.objects.create(
                slug=fake.slug(),
                name=fake.company(),
                symbol=fake.currency_code(),
                market_cap_presale=choice([True, False]),
                selected_auto_voting=choice([True, False]),
                votes=randint(0, 10000),
                votes24h=randint(0, 500),
                path_coin_img=random_image,  # Используем случайное изображение
            )

            # Привязка случайных labels
            selected_labels = sample(labels, k=randint(0, len(labels)))  # 0, 1 или 2 метки
            coin.labels.set(selected_labels)

            # AuditInfo
            AuditInfo.objects.create(
                coin=coin,
                audit_company=fake.company(),
                audit_link=fake.url(),
                doxxed=fake.url(),
            )

            # TaxInfo
            TaxInfo.objects.create(
                coin=coin,
                sell_tax=randint(0, 50),
                buy_tax=randint(0, 50),
                slippage=randint(0, 20),
            )

            # PresaleInfo
            PresaleInfo.objects.create(
                coin=coin,
                presale=choice([True, False]),
                softcap=f"{randint(1000, 5000)} USDT",
                hardcap=f"{randint(5000, 10000)} USDT",
                presale_link=fake.url(),
                presale_date=fake.date_between(start_date='-30d', end_date='+30d'),
                whitelist=choice([True, False]),
            )

            # CoinDescription
            CoinDescription.objects.create(
                coin=coin,
                desc_0=fake.text(),
                desc_1=fake.text(),
                desc_2=fake.text(),
                desc_3=fake.text(),
                desc_4=fake.text(),
                desc_5=fake.text(),
            )

            # CoinSocials
            for _ in range(randint(1, 3)):
                CoinSocials.objects.create(
                    coin=coin,
                    name=fake.word(),
                    link=fake.url(),
                    icon=None,  # Тут добавьте путь к изображению, если необходимо
                    is_active=choice([True, False]),
                )

            # ContractAddress
            for _ in range(randint(1, 2)):
                ContractAddress.objects.create(
                    coin=coin,
                    chain=choice(chains),
                    contract_address=fake.uuid4(),
                    basic=choice([True, False]),
                )

        self.stdout.write(self.style.SUCCESS(f"{amount} фейковых монет успешно создано!"))


# python manage.py create_fake_coins 10
