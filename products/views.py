from products._custom_order import CustomeOrderingFilter
from products.models import Product
from shopy.serializers import ProductSerializer

from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend


class PurchaseListAPIView(generics.ListAPIView):
    """
    PurchaseListAPIView
    Restful Structure:
        | URL style          | HTTP Method | URL Name    | Action Function |
        |------------------- |-------------|-------------|-----------------|
        | api/product/search | GET         | search      | product_list    |
    User пользуется фильтрами и сортировкой для добавления продуктов
    Добавить фильтрацию товаров по названию магазина.
    Добавить фильтрацию товаров по названию товара.
    Добавить сортировку по price_for_unit.
    Добавить сортировку по price_for_kg.
    """

    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, CustomeOrderingFilter]
    filterset_fields = ["shop_name__name", "name"]
    ordering_fields = ["price_for_unit", "price_for_kilo"]

    def get_queryset(self):
        queryset = Product.objects.all()
        product_required = self.request.query_params.get("product")
        if product_required is not None:
            queryset = queryset.filter(name=product_required)
        return queryset
