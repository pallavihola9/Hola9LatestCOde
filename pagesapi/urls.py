from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import ContactView

route = routers.DefaultRouter()
route.register("",ContactView,basename='contactview')

urlpatterns = [
    path('',include(route.urls)),
]

