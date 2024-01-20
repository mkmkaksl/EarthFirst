from django.templatetags.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("map", views.map, name="map"),
    path("tips", views.tips, name="tips")
]
