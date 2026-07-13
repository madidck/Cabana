from django.urls import path
from . import views

app_name = "cabanas"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("cabanas/", views.catalogo, name="catalogo"),
    path("cabanas/<str:clave>/", views.detalle_cabana, name="detalle"),
    path("nosotros/", views.nosotros, name="nosotros"),
    path("contacto/", views.contacto, name="contacto"),
    path("blog/", views.blog, name="blog"),
]
