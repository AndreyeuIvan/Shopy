from django.urls import include, path
from rest_framework import routers

from shopy import views


router = routers.DefaultRouter()

router.register(r'shopy', views.ReversedViewSet, basename='reserve')


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('basket/', views.BasketView.as_view()),
]
