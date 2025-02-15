from django.utils.text import slugify
from django.core.exceptions import ValidationError
from datetime import datetime

from app.models_db.coin import Chain, Coin, ContractAddress, AuditInfo, TaxInfo, PresaleInfo, CoinDescription, \
    CoinSocials


class CoinCreator:
    """
    Класс для обработки данных формы и сохранения новой монеты в базу данных.
    """
    def __init__(self, data, file=None):
        print(f"\n\nFORM Data Coin: {data}")
        print(f"\nFORM Data File: {file}")

        self.data = data
        self.file = file
        self.cleaned_data = {}

    @staticmethod
    def create_data_audit_info(**data_from_the_form):
        try:
            AuditInfo.objects.create(**data_from_the_form).save()
        except Exception as e:
            print(f"[DEBUG add_coin.py (26)]: {e}")

    @staticmethod
    def create_data_tax_info(**data_from_the_form):
        try:
            TaxInfo.objects.create(**data_from_the_form).save()
        except Exception as e:
            print(f"[DEBUG add_coin.py (33)]: {e}")

    @staticmethod
    def create_data_presale_info(**data_from_the_form):
        try:
            PresaleInfo.objects.create(**data_from_the_form).save()
        except Exception as e:
            print(f"[DEBUG add_coin.py (40)]: {e}")

    @staticmethod
    def create_data_description(**data_from_the_form):
        try:
            CoinDescription.objects.create(**data_from_the_form).save()
        except Exception as e:
            print(f"[DEBUG add_coin.py (47)]: {e}")

    @staticmethod
    def create_data_socials(**data_from_the_form):
        try:
            CoinSocials.objects.create(**data_from_the_form).save()
        except Exception as e:
            print(f"[DEBUG add_coin.py (54)]: {e}")

    def clean_data(self):
        """Обрабатывает и преобразует данные перед сохранением."""
        meta = {k: v for k, v in self.data.items() if k.startswith("meta[")}

        # Формируем slug из названия монеты
        name = self.data.get('post_title', '').strip()
        file_url = self.data.get('file_url', '').strip()

        self.cleaned_data['name'] = name
        self.cleaned_data['slug'] = slugify(name)
        self.cleaned_data['symbol'] = meta.get('meta[code]', '').upper()

        # Данные для модели AuditInfo:
        self.cleaned_data['audit_company'] = meta.get('meta[audit_companу]')
        self.cleaned_data['audit_link'] = meta.get('meta[audit_link]')
        self.cleaned_data['doxxed'] = meta.get('meta[doxxed]')

        # Данные для модели TaxInfo:
        self.cleaned_data['sell_tax'] = meta.get('meta[sell_tax]')
        self.cleaned_data['buy_tax'] = meta.get('meta[buy_tax]')
        self.cleaned_data['slippage'] = meta.get('meta[slippage]')

        # Данные для модели PresaleInfo:
        self.cleaned_data['presale'] = meta.get('meta[presale]')
        self.cleaned_data['softcap'] = meta.get('meta[softcap]')
        self.cleaned_data['presale_link'] = meta.get('meta[presale_link]')
        self.cleaned_data['hardcap'] = meta.get('meta[hardcap]')
        self.cleaned_data['presale_date'] = meta.get('meta[presale_date]')
        self.cleaned_data['whitelist'] = meta.get('meta[whitelist]')

        # Данные для модели CoinDescription:
        self.cleaned_data['desc_0'] = meta.get('meta[desc_0]')
        self.cleaned_data['desc_1'] = meta.get('meta[desc_1]')
        self.cleaned_data['desc_2'] = meta.get('meta[desc_2]')
        self.cleaned_data['desc_3'] = meta.get('meta[desc_3]')
        self.cleaned_data['desc_4'] = meta.get('meta[desc_4]')
        self.cleaned_data['desc_5'] = meta.get('meta[desc_5]')

        # Данные для модели CoinSocials:
        self.cleaned_data['reddit'] = meta.get('meta[reddit]')
        self.cleaned_data['twitter'] = meta.get('meta[twitter]')
        self.cleaned_data['gecko'] = meta.get('meta[gecko]')
        self.cleaned_data['discord'] = meta.get('meta[discord]')
        self.cleaned_data['market'] = meta.get('meta[market]')
        self.cleaned_data['website'] = meta.get('meta[website]')
        self.cleaned_data['github'] = meta.get('meta[github]')
        self.cleaned_data['youtube'] = meta.get('meta[youtube]')
        self.cleaned_data['tiktok'] = meta.get('meta[tiktok]')
        self.cleaned_data['medium'] = meta.get('meta[medium]')
        self.cleaned_data['instagram'] = meta.get('meta[instagram]')
        self.cleaned_data['telegram'] = meta.get('meta[telegram]')

        # Дата запуска (если есть)
        launch_date = meta.get('meta[launch_date]', '')
        if launch_date:
            try:
                self.cleaned_data['launch_date'] = datetime.strptime(launch_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("Некорректный формат даты")

        # Presale
        self.cleaned_data['market_cap_presale'] = meta.get('meta[presale]', '0') == '1'

        # Telegram (ссылки можно обработать позже)
        self.cleaned_data['telegram'] = meta.get('meta[telegram]', '')

        # Собираем все контрактные адреса
        contract_addresses = []
        index = 0
        while f"meta[contract_addresses_chain][{index}]" in meta and f"meta[contract_addresses][{index}]" in meta:
            chain_id = meta[f"meta[contract_addresses_chain][{index}]"]
            contract_address = meta[f"meta[contract_addresses][{index}]"]

            if chain_id and contract_address:
                chain = self.__get_chain(chain_id)
                contract_addresses.append({"chain": chain, "address": contract_address})

            index += 1

        self.cleaned_data['contract_addresses'] = contract_addresses

    @staticmethod
    def __get_chain(chain_id):
        """Получаем или создаем Chain по ID."""
        if not chain_id:
            return None
        chain = Chain.objects.get(id=int(chain_id))
        return chain

    def save(self):
        """Сохраняет монету и связанные контрактные адреса в базу данных."""
        self.clean_data()

        # Создаем объект Coin
        coin_data = {
            "name": self.cleaned_data['name'],
            "slug": self.cleaned_data['slug'],
            "symbol": self.cleaned_data['symbol'],
            "market_cap_presale": self.cleaned_data['market_cap_presale'],
            "launch_date": self.cleaned_data.get('launch_date'),
            "volume_usd": 0,
        }
        coin = Coin.objects.create(**coin_data)

        # Сохранение изображения (если загружено)
        if self.file:
            coin.path_coin_img = self.file
            coin.save(update_fields=["path_coin_img"])

        # Сохранение всех контрактных адресов
        contract_addresses = [
            ContractAddress(
                coin=coin,
                chain=contract_data['chain'],
                contract_address=contract_data['address'],
                basic=(index == 0)  # Первый будет True, остальные False
            )
            for index, contract_data in enumerate(self.cleaned_data['contract_addresses'])
        ]
        ContractAddress.objects.bulk_create(contract_addresses)

        self.create_data_audit_info(
            coin=coin,
            audit_company=self.cleaned_data.get('audit_company'),
            audit_link=self.cleaned_data.get('audit_link'),
            doxxed=self.cleaned_data.get('doxxed'),
        )

        self.create_data_tax_info(
            coin=coin,
            sell_tax=self.cleaned_data.get('sell_tax'),
            buy_tax=self.cleaned_data.get('buy_tax'),
            slippage=self.cleaned_data.get('slippage'),
        )

        # print(f"\n[DEBUG add_coin.py (208)] hardcap: {self.cleaned_data['hardcap']}")
        # print(f"[DEBUG add_coin.py (209)] audit_company: {self.cleaned_data['presale_link']}")
        self.create_data_presale_info(
            coin=coin,
            presale=self.cleaned_data.get('presale'),
            softcap=self.cleaned_data.get('softcap'),
            presale_link=self.cleaned_data.get('presale_link'),
            hardcap=self.cleaned_data.get('hardcap'),
            presale_date=self.cleaned_data.get('presale_date'),
            whitelist=self.cleaned_data.get('whitelist'),
        )

        self.create_data_description(
            coin=coin,
            desc_0=self.cleaned_data.get('desc_0'),
            desc_1=self.cleaned_data.get('desc_1'),
            desc_2=self.cleaned_data.get('desc_2'),
            desc_3=self.cleaned_data.get('desc_3'),
            desc_4=self.cleaned_data.get('desc_4'),
            desc_5=self.cleaned_data.get('desc_5'),
        )

        self.create_data_socials(
            coin=coin,
            reddit=self.cleaned_data.get('reddit'),
            twitter=self.cleaned_data.get('twitter'),
            gecko=self.cleaned_data.get('gecko'),
            discord=self.cleaned_data.get('discord'),
            market=self.cleaned_data.get('market'),
            website=self.cleaned_data.get('website'),
            github=self.cleaned_data.get('github'),
            youtube=self.cleaned_data.get('youtube'),
            tiktok=self.cleaned_data.get('tiktok'),
            medium=self.cleaned_data.get('medium'),
            instagram=self.cleaned_data.get('instagram'),
            telegram=self.cleaned_data.get('telegram'),
        )
        
        return coin

