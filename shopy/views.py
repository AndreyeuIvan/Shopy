from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from shopy._custome_order import CustomeOrderingFilter
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import views
from rest_framework import response
from rest_framework import status
from rest_framework import filters
from rest_framework import generics
from rest_framework import mixins

from shopy.serializers import ReserverSerializer, AccountSerializer, ProductSerializer
from shopy.models import Reserved, Account, Product


class ReversedReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = ReserverSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["product__name"]

    def get_queryset(self):
        return Reserved.objects.filter(user=self.request.user.id)


class BasketView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReserverSerializer
    # queryset = Product.objects.all()
    def get_serializer_context(self):
        return {"request": self.request}

    def post(self, request):
        """
        {
            "product":
                1,
            "number_of_units":1
        }
        """
        own_stock = Product.objects.get(id=request.data["product"])
        required_qty = request.data["number_of_units"]
        serializer = ReserverSerializer(
            data=request.data, context={"own_stock": own_stock.number_of_units}
        )
        if serializer.is_valid():
            own_stock = Product.objects.get(id=request.data["product"])
            required_qty = request.data["number_of_units"]
            own_stock.number_of_units = own_stock.number_of_units - required_qty
            own_stock.save()
            serializer.save(user_id=request.user.id)
            return response.Response(
                f"{serializer.data['number_of_units']} have been added to product_id {serializer.data['product']}",
                status=status.HTTP_201_CREATED,
            )
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        User выбирает товар, number_of_units, нажимает кнопку “Remove”
        и его товары удаляются из Reserved
        (увеличивается number_of_units в Storage).
        Количество товаров соотвественно юзеру
        """
        serializer = ReserverSerializer(data=request.data)
        if serializer.is_valid():
            product_pk = request.data["product"]
            qty_add_to_product = request.data["number_of_units"]
            product_to_increment_qty = get_object_or_404(Product, pk=product_pk)
            product_to_increment_qty.number_of_units = (
                product_to_increment_qty.number_of_units + qty_add_to_product
            )
            product_to_increment_qty.save()

            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    '''
    def patch(self, request):
        """
        User выбирает товар и нажимает кнопку “Delete”
        и все его товары одного вида удаляются из Reserved
        (увеличивается number_of_units в Storage).
        """
        serializer = ReserverSerializer(data=request.data)
        if serializer.is_valid():
            product_pk = request.data["product"]
            all_reserved_goods = Reserved.objects.filter(
                user_id=request.user.id, product=request.data["product"]
            )
            if len(all_reserved_goods) > 0:
                all_reserved_goods.delete()
            else:
                return response.Response(
                    "Fullfill your basket", status=status.HTTP_400_BAD_REQUEST
                )
            qty_add_to_product = request.data["number_of_units"]
            product_to_increment_qty = get_object_or_404(Product, pk=product_pk)
            product_to_increment_qty.number_of_units = (
                product_to_increment_qty.number_of_units + qty_add_to_product
            )
            product_to_increment_qty.save()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
    '''


class BasketDeleteView(BasketView, mixins.RetrieveModelMixin):
    def delete(self, request, *args, **kwargs):
        """
        User выбирает товар и нажимает кнопку “Delete”
        и все его товары одного вида удаляются из Reserved
        (увеличивается number_of_units в Storage).
        """
        serializer = ReserverSerializer(data=request.data)
        if serializer.is_valid():
            product_pk = kwargs["pk"]
            all_reserved_goods = Reserved.objects.filter(
                user_id=request.user.id, product=product_pk
            )
            for product in all_reserved_goods:
                product_to_increment_qty = get_object_or_404(Product, pk=product_pk)
                product_to_increment_qty.number_of_units += product.number_of_units
                product_to_increment_qty.save()
                product.delete()
            if len(all_reserved_goods) == 0:
                return response.Response(
                    "Fullfill your basket", status=status.HTTP_400_BAD_REQUEST
                )
        return response.Response(
            "Balance has been restored", status=status.HTTP_204_NO_CONTENT
        )


class BuyGenericAPIView(generics.GenericAPIView):
    """Userviewset
    Restful Structure:
        | URL style      | HTTP Method | URL Nanme   | Action Function |
        |----------------|-------------|-------------|-----------------|
        | /users         | GET, POST   | user-list   | user_list       |
        | /users/<email> | GET, DELETE | user-detail | user_detail     |
    """
    queryset = Reserved.objects.all()
    serializer_class = ReserverSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        """
        User нажимает кнопку “Buy” и все его товары удаляются из Reserved и списываются деньги с Account.
        Как только создается юзер- создавать аккаунт
        """
        queryset_of_products = Reserved.objects.filter(user=request.user.id)
        print(request.user)
        # import pdb;pdb.set_trace()
        sum_reserved = sum([x.total_price for x in queryset_of_products])
        account_serializer = AccountSerializer(
            data=request.data,
            context={
                "sum_reserved": sum_reserved,
                "account_amount": request.user.account.amount,
            },
        )
        if sum_reserved == 0:
            return response.Response(
                "You have no reserved items in a basket.",
                status=status.HTTP_404_NOT_FOUND,
            )
        elif account_serializer.is_valid():
            [x.delete() for x in queryset_of_products]
            return response.Response(
                "You reserved items in a basket has been deleted.",
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return response.Response(
                account_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class ClearGenericAPIView(generics.GenericAPIView):
    queryset = Reserved.objects.all()
    serializer_class = ReserverSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        """
        ClearGenericAPIView
        Restful Structure:
        | URL style          | HTTP Method | URL Nanme   | Action Function |
        |------------------- |-------------|-------------|-----------------|
        | api/clear/         | DELETE      | clear       | reserved_delete |
        User нажимает кнопку “Clear” и все его товары удаляются из
        Reserved (увеличивается number_of_units в Storage).
        Bulk_update(number_of_units)
        """
        import pdb;pdb.set_trace()
        list_of_products_reversed = Reserved.objects.filter(user=request.user.id)
        for reservation in list_of_products_reversed:
            product = reservation.product
            product.number_of_units += reservation.number_of_units
            # reservation.delete() -> сохранить в отдельный список и удалить
            product.save()  # изменить bulk_update
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseListAPIView(generics.ListAPIView):
    """
    PurchaseListAPIView
    Restful Structure:
        | URL style          | HTTP Method | URL Nanme   | Action Function |
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
        product_required = self.request.query_params.get('product')
        if product_required is not None:
            queryset = queryset.filter(name=product_required)
        return queryset
