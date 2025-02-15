from django.http import HttpRequest

from django.shortcuts import render

from app.controllers_views.page_coin import CoinPageContextManager


def coin(request: HttpRequest, chain_slug, coin_slug):
    context = CoinPageContextManager(request=request, chain_slug=chain_slug, coin_slug=coin_slug).get_context()
    return render(request, template_name='app/token-card.html', context=context, status=200)

