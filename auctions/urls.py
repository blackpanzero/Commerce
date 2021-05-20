from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<str:category>", views.category, name="category"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("new/", views.new, name="new"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("add_watchlist/<int:listing_id>",views.add_watchlist,name="add_watchlist"),
    path("watchlist/",views.watchlist,name="watchlist"),
    path("remove_watchlist/<int:listing_id>",views.remove_watchlist,name="remove_watchlist"),
    path("close_auction/<int:listing_id>",views.close_auction,name="close_auction"),
    path("auctions/", views.auctions, name="auctions"),

]
