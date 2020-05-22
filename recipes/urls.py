from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
from .api import views as api_views
# https://www.django-rest-framework.org/tutorial/quickstart/#quickstart

urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('<int:recipe_id>/', views.detail, name='detail'),
	path('new/', views.new, name='new'),
	path('api/new/', api_views.new)
] + staticfiles_urlpatterns()