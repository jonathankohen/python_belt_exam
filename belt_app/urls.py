from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('quotes', views.quotes),
    path('add_quote', views.add_quote),
    path('delete_quote/<int:quote_id>', views.delete_quote),
    path('like_quote/<int:quote_id>', views.like_quote),
    path('user/<int:user_id>', views.show_user),
    path('myaccount/<int:user_id>', views.edit_acct),
    path('make_changes/<int:user_id>', views.make_changes),
]
