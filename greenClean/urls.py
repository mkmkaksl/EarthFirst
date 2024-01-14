from django.templatetags.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("map", views.mapForm, name="mapForm"),
    path("map/<int:year>", views.mapView, name="mapView"),
    path("tips", views.tips, name="tips")
]
