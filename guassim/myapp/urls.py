from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.views.static import serve
from django.conf import settings
from . import views
app_name = "myapp"

urlpatterns = [
    path("", views.app_index, name="app_index"),
    path("about/", views.page_about, name="page_about"), 
    path('category/<slug:slug>', views.category_detail, name='category_detail'),
    path('collection/<slug:slug>', views.collection_detail, name='collection_detail'),
    path('collection/create_favorite/', views.create_favorite, name='create_favorite'),
    path('contact/', views.page_contact, name='page_contact'),
    path('photo/id/<int:pk>', views.photo_detail, name='photo_detail'),
]
