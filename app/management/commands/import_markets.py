import json
from django.core.management.base import BaseCommand

from app.models_db.coin import Market, ChainMarket, Chain


class Command(BaseCommand):
    help = "Импорт данных в модели ChainMarket и Market из JSON файла"

    def handle(self, *args, **kwargs):
        # Открываем JSON файл
        try:
            with open("markets_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("Файл markets_data.json не найден"))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Ошибка при чтении JSON файла"))
            return

        # Сбрасываем старые данные (опционально)
        Market.objects.all().delete()
        ChainMarket.objects.all().delete()

        # Импортируем данные из файла
        for chain_market_data in data:
            # Получаем Chain
            chain, created = Chain.objects.get(name=chain_market_data["chain"])

            # Создаём ChainMarket
            chain_market = ChainMarket.objects.create(chain=chain)

            # Создаём Markets
            for market_data in chain_market_data["markets"]:
                # Если у market_data["image"] есть значение, оно будет записано как имя файла
                Market.objects.create(
                    market=chain_market,
                    name_market=market_data["name_market"],
                    url_template=market_data["url_template"],
                    image=market_data["image"],  # Передаём имя файла, и Django сформирует путь
                    description=market_data["description"],
                )

        self.stdout.write(self.style.SUCCESS("Данные успешно импортированы из файла markets_data.json"))


# python manage.py import_markets
