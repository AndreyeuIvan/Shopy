from django.urls import re_path

from products import views


urlpatterns = [
    re_path(r"^search/?$", views.PurchaseListAPIView.as_view(), name="search"),
]
