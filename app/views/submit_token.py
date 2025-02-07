from django.http import HttpRequest
from django.shortcuts import render

from app.controllers_views.controllers_base import BaseContextManager


def add_coin(request: HttpRequest):
    base_context = BaseContextManager(request).get_context()
    return render(request=request, template_name='app/add-coin.html', context=base_context, status=200)


def add_coin2(request: HttpRequest):
    base_context = BaseContextManager(request).get_context()
    return render(request=request, template_name='app/add-coin2.html', context=base_context, status=200)


def add_coin3(request: HttpRequest):
    base_context = BaseContextManager(request).get_context()
    return render(request=request, template_name='app/add-coin3.html', context=base_context, status=200)

