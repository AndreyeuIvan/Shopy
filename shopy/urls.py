from django.urls import include, path
from rest_framework import routers

from shopy import views


router = routers.DefaultRouter()

router.register(r'shopy', views.ReversedViewSet, basename='reserve')
router.register(r'account', views.AccountReadOnlyViewSet)
router.register(r'product', views.ProductReadOnlyViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('basket/', views.BasketView.as_view()),
]
