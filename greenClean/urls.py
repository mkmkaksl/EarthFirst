from django.templatetags.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("map", views.map, name="map"),
    path("tips", views.tips, name="tips"),
    path("footprint", views.footprintCalculator, name="footprintCalculator"),
    path("contact", views.contact, name="contact"),
    path("solutions", views.solutions, name="solutions"),
    path("moreinfo", views.moreinfo, name="moreinfo"),
    path("documentation", views.documentation, name="documentation")
]
