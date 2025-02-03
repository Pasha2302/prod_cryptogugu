from django.urls import path

from app.views import index_view
from app.views import coin_view


urlpatterns = [
    # ----------------------------------- Path Index Page ---------------------------------------------------- #
    path("", index_view.index, name="index"),
    path("header-search-component/", index_view.get_header_search_component, name="header_search_component"),
    path(
        "table-promoted-coins-component/",
        index_view.get_table_promoted_coins_component,
        name="get_table_promoted_coins_component"
    ),
    path("show-more/", index_view.show_more, name="show_more"),
    path("voting/", index_view.voting, name="voting"),

    path("airdrops/", index_view.airdrops, name="airdrops"),
    path("promote/", index_view.promote, name="promote"),
    path("careers/", index_view.careers, name="careers"),
    path("partners/", index_view.partners, name="partners"),
    path("contact-us/", index_view.contact, name="contact"),

    # ----------------------------------- Path Coin Page ---------------------------------------------------- #

    path('coin/<str:chain>/<slug:slug>/', coin_view.coin, name="coin"),

    # ----------------------------------- Paths Blog Page --------------------------------------- #

    path("blog/", index_view.blog, name="blog"),

    # ----------------------------------- Different Paths (разные пути)--------------------------------------- #
    path("get-user-id/", index_view.get_user_id, name="get_user_id"),
    path("set-theme-site/", index_view.set_theme_site, name="set_theme_site"),

    path("clear-settings/", index_view.clear_settings, name="clear_settings"),
    path("reset-all-votes/", index_view.reset_all_votes, name="reset_all_votes"),

]
