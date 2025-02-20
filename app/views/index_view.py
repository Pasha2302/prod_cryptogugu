import json

from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpRequest, JsonResponse, HttpResponse

from django.views import View

# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page

from app.controllers_views.base import BaseContextManager
from app.controllers_views.header_search import HeaderSearchManager
from app.controllers_views.page_index import IndexContextManager, PromotedCoinsContextManager, VoteManager
from app.controllers_views.settings_user import clear_data, save_user, SettingsManager
from app.models_db.coin import Coin


class IndexView(View):
    def post(self, request: HttpRequest):
        context = IndexContextManager(request).get_context()

        html_data = render_to_string('app/components_html/coins_trending_component.html', context)
        pagination_html = render_to_string('app/components_html/pagination_component.html', context)
        data = {'html': html_data, 'pagination': pagination_html}
        return JsonResponse(data, status=200)

    # @method_decorator(cache_page(60 * 60 * 12))  # Кэшировать GET-запросы на 12 часов
    def get(self, request: HttpRequest):
        context = IndexContextManager(request).get_context() | BaseContextManager(request).get_context()
        # print(f"\nDEBUG index_view.py (34): < IndexView.get()\n> context: {context} >")

        response = render(request, 'app/index.html', context=context, status=200)
        # кэширован в промежуточных кэшах на 1 час, но после этого должен быть проверен на актуальность с сервером:
        # response['Cache-Control'] = 'public, max-age=6600'
        return response


def show_more(request: HttpRequest):
    if request.method == 'POST':
        user_id_str = request.COOKIES.get('userId')
        current_page = json.loads(request.body)['data']['morePage']
        print(f"\n[show_more() method = 'POST']:\nData POST: {current_page=}\nUser ID: {user_id_str}")

        context = IndexContextManager(request).get_context()
        html_data = render_to_string(
            template_name='app/components_html/coins_trending_component.html',
            context=context,
        )
        data = {'coins_html': html_data}
        return JsonResponse(data=data, status=200)
    else:
        return JsonResponse(data={'status': 'Incorrect request'}, status=402)


def get_header_search_component(request: HttpRequest):
    if request.method == 'POST':
        context = HeaderSearchManager(request).get_context()
        html_data = render_to_string('app/components_html/header_search_component.html', context)
        data = {'coins_html': html_data}
        return JsonResponse(data=data, status=200)
    else:
        return JsonResponse(data={'status': 'Incorrect request'}, status=402)


def get_table_promoted_coins_component(request: HttpRequest):
    if request.method == 'POST':
        context = PromotedCoinsContextManager(request).get_context()
        print(f"\n\n[Promoted Coins Component]\n{context=}")
        if context is None:
            return JsonResponse(data={'coins_html': ""}, status=200)

        html_data = render_to_string('app/components_html/table_coins_component.html', context)
        data = {'coins_html': html_data}
        return JsonResponse(data=data, status=200)
    else:
        return JsonResponse(data={'status': 'Incorrect request'}, status=402)


def voting(request: HttpRequest):
    if request.method == 'POST':
        vote_manager = VoteManager(request=request)
        vote_manager.check_and_save_vote()
        data_vote = vote_manager.get_data_vote()
        return JsonResponse(data=data_vote, status=200)
    else:
        return JsonResponse(data={'status': 'Incorrect request'}, status=402)


# -------------------------------------------------------------------------------------------------------------------- #

def airdrops(request: HttpRequest):
    base_context = BaseContextManager(request).get_context()
    return render(request, 'app/airdrops.html', context=base_context, status=200)


def promote(request: HttpRequest):
    base_context = BaseContextManager(request).get_context()
    return render(request, 'app/promote.html', context=base_context, status=200)


def careers(request: HttpRequest):
    base_context = BaseContextManager(request).get_context()
    return render(request, 'app/careers.html', context=base_context, status=200)


def partners(request: HttpRequest):
    base_context = BaseContextManager(request).get_context()
    return render(request, 'app/partners.html', context=base_context, status=200)


def contact(request: HttpRequest):
    base_context = BaseContextManager(request).get_context()
    return render(request, 'app/contact-us.html', context=base_context, status=200)


def blog(request: HttpRequest):
    base_context = BaseContextManager(request).get_context()
    return render(request=request, template_name='app/blog.html', context=base_context, status=200)


def terms_and_conditions(request: HttpRequest):
    base_context = BaseContextManager(request).get_context()
    return render(request=request, template_name='app/terms_and_conditions.html', context=base_context, status=200)


def privacy_policy(request: HttpRequest):
    base_context = BaseContextManager(request).get_context()
    return render(request=request, template_name='app/privacy_policy.html', context=base_context, status=200)


# =====================================================================================================================


def handler404(request: HttpRequest, exception):
    print("\nHandler 404")
    return render(request, 'app/example/404.html', status=404)


def clear_settings(request: HttpRequest):
    clear_data()
    return HttpResponse("All user settings have been cleared.")


def reset_all_votes(request: HttpRequest):
    Coin.objects.update(votes=0)
    Coin.objects.update(votes24h=0)
    Coin.objects.update(selected_auto_voting=False)
    return JsonResponse({'data': 'Голосование обнулено'}, status=200)


def get_user_id(request: HttpRequest):
    user_id = request.COOKIES.get('userId')
    data = save_user(user=user_id)
    return JsonResponse(data, status=200)


def set_theme_site(request: HttpRequest):
    if request.method == 'POST':
        SettingsManager(request)
        data = {'data': 'done | scheme installed'}
        return JsonResponse(data, status=200)
