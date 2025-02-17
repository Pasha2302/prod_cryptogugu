from django.http import HttpRequest, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render

from app.controllers_views.base import BaseContextManager
from app.controllers_views.page_index import IndexContextManager

from django.views import View


class ChainView(View):
    def post(self, request: HttpRequest):

        context = IndexContextManager(request).get_context()

        html_data = render_to_string('app/components_html/coins_trending_component.html', context)
        pagination_html = render_to_string('app/components_html/pagination_component.html', context)
        data = {'html': html_data, 'pagination': pagination_html}
        return JsonResponse(data, status=200)

    # @method_decorator(cache_page(60 * 60 * 12))  # Кэшировать GET-запросы на 12 часов
    def get(self, request: HttpRequest, chain_slug: str):
        print(f"\n[ChainView.get()] chain_slug: {chain_slug}")
        context = IndexContextManager(request, chain_slug).get_context() | BaseContextManager(request).get_context()
        # print(f"\nDEBUG index_view.py (34): < IndexView.get()\n> context: {context} >")

        response = render(
            request,
            template_name='app/components_html/coins/tables/chain_coin_com.html',
            context=context,
            status=200
        )
        # кэширован в промежуточных кэшах на 1 час, но после этого должен быть проверен на актуальность с сервером:
        # response['Cache-Control'] = 'public, max-age=6600'
        return response

