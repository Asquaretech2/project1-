from django.urls import path
from . import views


urlpatterns =[
    path('', views.index, name='index'),
    path('creator/', views.creator, name='creator'),
    path('contact/', views.contact, name='contact'),
    path('FAQ/', views.faq, name='FAQ'),
    path('Privacy/', views.Privacy, name='Privacy'),
    path('reviews/',views.reviews, name='reviews'),
    path('terms/', views.terms, name='terms'),
]