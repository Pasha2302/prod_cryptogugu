from django.core.exceptions import ValidationError
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from app.controllers_views.base import BaseContextManager
from app.controllers_views.add_coin import CoinCreator
from app.models_db.coin import Chain


def add_coin(request: HttpRequest):
    if request.method == 'POST':
        data_add_coin = request.POST.dict()
        file = request.FILES.get('file')  # Получаем загруженное изображение

        try:
            coin_creator = CoinCreator(data_add_coin, file)
            new_coin = coin_creator.save()
            return JsonResponse({'coin_success': 1, 'coin_id': new_coin.id}, status=200)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=201)

    else:
        base_context = BaseContextManager(request).get_context()
        base_context['cains'] = Chain.objects.all()
        return render(
            request=request,
            template_name='app/components_html/coins/add/add-coin.html',
            context=base_context,
            status=200
        )

