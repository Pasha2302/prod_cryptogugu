import json
from django.core.management.base import BaseCommand

from app.models_db.coin import ChainMarket, Market


class Command(BaseCommand):
    help = "Экспорт данных из моделей ChainMarket и Market в JSON файл"

    def handle(self, *args, **kwargs):
        # Список для хранения данных
        data = []

        # Получаем все ChainMarket и связанные Markets
        for chain_market in ChainMarket.objects.all():
            chain_market_data = {
                "chain": chain_market.chain.name,  # Название чейна
                "markets": []
            }

            # Добавляем все Markets, связанные с ChainMarket
            markets = Market.objects.filter(market=chain_market)
            for market in markets:
                chain_market_data["markets"].append({
                    "name_market": market.name_market,
                    "url_template": market.url_template,
                    "image": market.image.name if market.image else None,  # Сохраняем только имя файла
                    "description": market.description,
                })

            # Добавляем данные ChainMarket в итоговый список
            data.append(chain_market_data)

        # Сохраняем данные в JSON файл
        with open("markets_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        self.stdout.write(self.style.SUCCESS("Данные успешно экспортированы в файл markets_data.json"))


# python manage.py export_markets
