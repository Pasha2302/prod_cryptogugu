from django.db import transaction
from django.http import HttpRequest

from django.db.models import F
from django.shortcuts import render, get_object_or_404

from app.controllers_views.controllers_base import BaseContextManager
from app.models import Coin


def coin(request: HttpRequest, chain, slug):
    with transaction.atomic():
        # Обновляем счётчик просмотров
        Coin.objects.filter(chain=chain, slug=slug).update(views=F('views') + 1)
        # Получаем объект монеты с уже обновлённым значением views
        coin_obj = get_object_or_404(Coin, chain=chain, slug=slug)

    base_context = BaseContextManager(request).get_context()
    context = base_context | {"coin": coin_obj}
    return render(request, template_name='app/token-card.html', context=context, status=200)

