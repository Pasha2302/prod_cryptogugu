from django import template
import logging
from app.models_db.coin import Coin

register = template.Library()
logger = logging.getLogger('coin_tags')


@register.simple_tag
def get_chain(coin: Coin) -> str:
    """
    Возвращает slug цепочки (chain.slug) для переданной монеты (coin).
    Если связь не найдена, возвращает 'unknown-slug'.
    """
    return coin.get_chain_from_basic_contract()

