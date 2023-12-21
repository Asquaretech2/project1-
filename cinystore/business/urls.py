from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('otp_page/', views.otp_page, name='otp_page'),
    path('register_page/', views.register_page, name='register_page'),
    path('select_page/', views.select_page, name='select_page'),
    path('welcome_page/', views.welcome_page, name='welcome_page'),
    path('businessBase/', views.businessBase, name='businessBase'),
    path('corporateBase/', views.corporateBase, name='corporateBase'),
    path('corporateHome/', views.corporateHome, name='corporateHome'),
    path('Individual_page/', views.Individual_page, name='Individual_page'),
    path('corporate_page/', views.corporate_page, name='corporate_page'),
    path('ott_page/', views.ott_page, name='ott_page'),
    path('agency_page/', views.agency_page, name='agency_page'),
    #path('login_otp/', views.login_otp, name="login_otp"),
    path('business/', views.Business, name="business"),

    # path('verify_otp/', views.verify_otp, name='verify_otp'),
]