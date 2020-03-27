from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    path('dashboard', views.dashboard),
    path('create', views.create),

    path('edit/<int:id>', views.update),
    path('delete/<int:id>', views.delete),
]
