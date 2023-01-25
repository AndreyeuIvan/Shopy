from django.db.models.query import QuerySet

from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import response
from rest_framework import status

from shopy.serializers import ReserverSerializer, AccountSerializer, ProductSerializer
from shopy.models import Reserved, Account, Product


class ReversedViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing and editing the accounts
    associated with the user.
    """

    serializer_class = ReserverSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Reserved.objects.filter(user=self.request.user.id)


class AccountReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class ProductReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class BasketView(APIView):
    #http_method_names = ['POST', 'PUT', 'DELETE']
    
    def post(self, request):
        """
        {"product_id": 1,
        "number_of_units":1}
        """
        data = {
            "product": 1,
            "number_of_units":1
        }
        import pdb;pdb.set_trace()
        serializer = ReserverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        pass
    
    def delete(self, request):
        pass
    
    