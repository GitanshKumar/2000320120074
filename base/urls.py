from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('trains', views.getTrainsData, name="trains"),
    path('trains/<str:pk>', views.getTrainData, name="train"),
]