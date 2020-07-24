from django.urls import path
from . import views

urlpatterns = [
    path('', views.wall),
    path('create', views.create),
    path('comment/create/<int:id>', views.create_comment),
    path('comment/delete/<int:id>', views.delete),
]