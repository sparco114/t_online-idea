"""
URL configuration for conf project.

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
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from autoru_catalog.views import MarksListView, ModelsOfMarkListView, UpdateAutoruCatalogView

# router = SimpleRouter()

# router.register('car_marks_list', MarksListView)
# router.register('mark_models_list/<int:pk>', ModelsOfMarkListView, basename='mark_models_list')
# router.register('update_autoru_catalog', UpdateAutoruCatalogView, basename='update_autoru_catalog')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('car_marks_list/', MarksListView.as_view({'get': 'list'})),
    path('mark_models_list/<int:mark_pk>/', ModelsOfMarkListView.as_view({'get': 'list'})),
    path('update_autoru_catalog/', UpdateAutoruCatalogView.as_view({'get': 'list'}))
]

# urlpatterns += router.urls
