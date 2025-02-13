import json
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from app.models import Coin


class Command(BaseCommand):
    help = 'Load coins from JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        with open(json_file, 'r') as file:
            data = json.load(file)

        for item in data:
            # Преобразование launch_date из строки в дату
            # launch_date = None
            # if item['launch_date']:
            #     try:
            #         launch_date = datetime.strptime(item['launch_date'], '%d/%m/%Y').date()
            #     except ValueError:
            #         self.stderr.write(self.style.ERROR(f"Invalid date format for launch_date: {item['launch_date']}"))

            # Создание и сохранение экземпляра Coin
            market_cap_presale = item['market_cap_presale'] if item['market_cap_presale'] else False
            price = item['price'] if float(item['price']) != 0 else None

            if item.get('market_cap'):
                market_cap = item['market_cap'] if float(item['market_cap']) != 0 else None
            else: market_cap = None

            coin = Coin(
                name=item['name'],
                symbol=item['symbol'],
                contract_address=item['contract_address'],
                tags=item.get('tags', []),
                chain=item['chain'],
                market_cap=market_cap,
                price=price,
                volume_usd=item['volume_usd'],
                volume_btc=item['volume_btc'],
                price_change_24h=item['price_change_24h'],
                votes=item['votes'],
                votes24h=item['votes24h'],
                path_coin_img=self.extract_filename(item['path_coin_img'], coin=True),
                path_chain_img=self.extract_filename(item['path_chain_img']),
                launch_date=item['launch_date'],
                market_cap_presale=market_cap_presale,
                launch_date_str=item.get('launch_date_str', None)
            )
            coin.save()
            self.stdout.write(self.style.SUCCESS(f"Coin {coin.name} saved successfully"))

    @staticmethod
    def extract_filename(old_path: str, coin=False) -> str | None:
        """
        Извлекает имя файла из старого пути и формирует новый путь.
        """
        path_dir_img = 'coin_images' if coin else 'chain_images'

        if not old_path:
            return None  # Если путь пустой, просто возвращаем None
        filename = os.path.basename(old_path)  # Достаем имя файла
        return f"{path_dir_img}/{filename}"  # Новый путь (Django сам добавит MEDIA_ROOT)


# /home/pavelpc/PycharmProjects/Working_Projects/Django_Cryptogugu/cryptogugu/app/management/commands/coins_data.json
# python manage.py load_coins path/to/your/jsonfile.json
