from django.urls import include, path, re_path
from rest_framework import routers

from shopy import views


router = routers.DefaultRouter()

router.register(r"basket", views.BasketViewSet, basename="basket")
# router.register(r'account', views.AccountReadOnlyViewSet)
# router.register(r'product', views.ProductReadOnlyViewSet, basename='product')


urlpatterns = [
    path("", include(router.urls)),
    # path('api-auth/', include('rest_framework.urls')),
    # path("basket/<int:pk>/", views.BasketGenericAPIView.as_view(), name='basket-detail'),  # basket_view переопределить Названия урлов
    path("annulment/", views.AnnulmentGenericAPIView.as_view(), name="annulment"),
    re_path(r"^product/search/?$", views.PurchaseListAPIView.as_view(), name="search"),
]
