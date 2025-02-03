import json
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from app.models import BaseCoin


class Command(BaseCommand):
    help = 'Load base coins from JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        with open(json_file, 'r') as file:
            data = json.load(file)

        for item in data:
            # Преобразование launch_date из строки в дату
            created_at = None
            if item.get('created_at'):
                try:
                    created_at = datetime.strptime(item['created_at'], '%d/%m/%Y').date()
                except ValueError:
                    self.stderr.write(self.style.ERROR(f"Invalid date format for created_at: {item['created_at']}"))

            # Создание и сохранение экземпляра BaseCoin
            base_coin = BaseCoin(
                name=item['name'],
                symbol=item['symbol'],
                contract_address=item.get('contract_address', None),
                pair_url=item.get('pair_url', None),
                market_cap=item.get('market_cap', None),
                price=item.get('price', None),
                volume_usd=item['volume_usd'],
                volume_btc=item['volume_btc'],
                price_change_24h=item['price_change_24h'],
                path_coin_img=self.extract_filename(item['path_coin_img'], coin=True),
                path_chain_img=self.extract_filename(item['path_chain_img']),
                created_at=created_at
            )
            base_coin.save()
            self.stdout.write(self.style.SUCCESS(f"BaseCoin {base_coin.name} saved successfully"))

    @staticmethod
    def extract_filename(old_path: str, coin=False) -> str | None:
        """
        Извлекает имя файла из старого пути и формирует новый путь.
        """
        path_dir_img = 'base_coin_images' if coin else 'chain_images'

        if not old_path:
            return None  # Если путь пустой, просто возвращаем None
        filename = os.path.basename(old_path)  # Достаем имя файла
        return f"{path_dir_img}/{filename}"  # Новый путь (Django сам добавит MEDIA_ROOT)


# /home/pavelpc/PycharmProjects/Working_Projects/Django_Cryptogugu/cryptogugu/app/management/commands/base_coins_data.json
# python manage.py load_base_coins path/to/your/jsonfile.json
