from django.urls import path
from . import views


urlpatterns =[
    path('market_signup/', views.market_signup, name='market_signup'),
    path('market_login/', views.market_login, name='market_login'),
    path('market_Logout/', views.market_Logout, name='market_Logout'),
    path('activate2/<uid64>/<token>', views.activate2, name='activate2'),
    path('marketing_dashboard/', views.marketing_dashboard, name='marketing_dashboard'),
    path('otp/', views.otp, name='otp'),
]