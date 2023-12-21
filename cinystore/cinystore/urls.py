"""
URL configuration for cinystore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from cinystoreapp import views
from django.conf import settings
from corporate import views
from business import views
from marketing import views
from cinystoreapp import models
from django.conf.urls import handler404, handler403
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from cinystoreapp.sitemaps import StaticViewSitemap
from django.contrib.sites.models import Site
from django.views.generic.base import TemplateView




sitemaps = {
    'sitemaps': StaticViewSitemap,
}



# sitemaps = {
#     'cinystoreapp': GenericSitemap(
#         {'queryset': models.objects.all()},  # Replace "YourModel" with the name of your model
#         priority=0.5,  # Set the priority for your model's URLs
#         changefreq='weekly'  # Set the change frequency for your model's URLs
#     )
# }


urlpatterns = [
    path('', include('cinystoreapp.urls')),
    path('corporate/', include('corporate.urls')),
    path('business/', include('business.urls')),
    path('marketing/', include('marketing.urls')),
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'cinystoreapp.views.page_not_found'
# handler500 = 'cinystoreapp.views.custom_500'
#handler403 = 'cinystoreapp.views.custom_permission_denied'


'''
urlpatterns += [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]'''
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)









