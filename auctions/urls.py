from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.listing, name="listing"),
    path("profile", views.profile, name="profile"),
    path("listing/<int:product_id>", views.product, name="product"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category", views.category, name="category"),
    path("category/<str:category_name>", views.specific_category, name="specific_category")
]
