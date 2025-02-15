from django.core.management.base import BaseCommand

from app.models_db.coin import Chain


CHAINS = [
    (87, "Algorand"),
    (97, "Aptos"),
    (75, "Arbitrum"),
    (88, "Avalanche"),
    (70, "Base"),
    (53, "Binance Smart Chain"),
    (90, "Blast"),
    (65, "Cardano"),
    (93, "CORE"),
    (79, "Cronos"),
    (94, "Dogechain"),
    (95, "Dragonfly-Chain"),
    (54, "Ethereum"),
    (76, "EthereumFair"),
    (82, "Fantom"),
    (80, "Harmony"),
    (85, "ICP"),
    (84, "Kaspa"),
    (81, "Kronobit"),
    (86, "Lunarium"),
    (89, "Mantle"),
    (68, "Polygon"),
    (77, "PulseChain"),
    (83, "Shibarium"),
    (55, "Solana"),
    (96, "SUI"),
    (69, "TON"),
    (74, "Tron"),
]


class Command(BaseCommand):
    help = "Добавляет цепочки блокчейнов в базу данных"

    def handle(self, *args, **kwargs):
        for chain_id, name in CHAINS:
            chain, created = Chain.objects.get_or_create(id=chain_id, defaults={"name": name})
            if created:
                self.stdout.write(self.style.SUCCESS(f"Добавлена цепочка: {name} (ID: {chain_id})"))
            else:
                self.stdout.write(self.style.WARNING(f"Цепочка уже существует: {name} (ID: {chain_id})"))


# python manage.py add_chains_comm
