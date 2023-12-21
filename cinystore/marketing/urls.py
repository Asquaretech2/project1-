from django.urls import path
from . import views


urlpatterns =[
    path('', views.index, name='index'),
    path('market_signup/', views.market_signup, name='market_signup'),
    path('market_login/', views.market_login, name='market_login'),
]