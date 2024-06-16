from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("save/<str:name>/<str:email>", views.save, name="save"),
    path("form/", views.form, name="form"),
    path("submit/", views.submit, name="submit"),
    path("<int:id>/salesman/", views.info, name="info"),
    path("products/<int:id>/", views.products, name='products'),
    path("products/", views.products, name='products')
]