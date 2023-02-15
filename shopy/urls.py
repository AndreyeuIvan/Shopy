from django.urls import include, path, re_path
from rest_framework import routers

from shopy import views


router = routers.DefaultRouter()

router.register(r"basket", views.BasketViewSet, basename="basket")


urlpatterns = [
    path("", include(router.urls)),
    path("annulment/", views.AnnulmentGenericAPIView.as_view(), name="annulment"),
]
