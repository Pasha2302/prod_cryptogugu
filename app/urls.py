from django.urls import path

from app.views import coin_view
from app.views.chain_view import ChainView
from app.views.email_subscribe import subscribe
from app.views.index_view import (
    IndexView, blog, get_user_id, get_header_search_component, get_table_promoted_coins_component, show_more, voting,
    airdrops, promote, careers, partners, contact, set_theme_site, clear_settings, reset_all_votes,
    terms_and_conditions, privacy_policy
)
from app.views.add_coin_view import add_coin

urlpatterns = [
    # ----------------------------------- Path Index Page ---------------------------------------------------- #
    path("", IndexView.as_view(), name="index"),
    path("header-search-component/", get_header_search_component, name="header_search_component"),
    path(
        "table-promoted-coins-component/",
        get_table_promoted_coins_component,
        name="get_table_promoted_coins_component"
    ),
    path("show-more/", show_more, name="show_more"),
    path("voting/", voting, name="voting"),

    path("airdrops/", airdrops, name="airdrops"),
    path("promote/", promote, name="promote"),
    path("careers/", careers, name="careers"),
    path("partners/", partners, name="partners"),
    path("contact-us/", contact, name="contact"),

    path("terms-and-conditions/", terms_and_conditions, name="terms_and_conditions"),
    path("privacy-policy/", privacy_policy, name="privacy_policy"),

    # ----------------------------------- Path Coin Page ---------------------------------------------------- #

    path('coin/<slug:chain_slug>/<slug:coin_slug>/', coin_view.coin, name="coin"),

    path('coin/<slug:chain_slug>/', ChainView.as_view(), name="chain_coin"),

    # ----------------------------------- Paths Blog Page --------------------------------------------------- #

    path("blog/", blog, name="blog"),

    # ----------------------------------- Different Paths (разные пути)--------------------------------------- #
    path("get-user-id/", get_user_id, name="get_user_id"),
    path("set-theme-site/", set_theme_site, name="set_theme_site"),

    path("clear-settings/", clear_settings, name="clear_settings"),
    path("reset-all-votes/", reset_all_votes, name="reset_all_votes"),

    # --------------------------------------- Mail Subscribe ------------------------------------------------- #

    path('subscribe/', subscribe, name='subscribe'),

    # --------------------------------------- Add Coin Page ------------------------------------------------- #

    path("add-coin/", add_coin, name="add_coin"),

]
