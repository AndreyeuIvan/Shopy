from django.db.models.query import QuerySet

from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.views import APIView

from shopy.serializers import ReserverSerializer
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


class BasketView(APIView):
    #http_method_names = ['POST', 'PUT', 'DELETE']
    
    def post(self, request):
        import pdb;pdb.set_trace()
        pass
    
    def put(self, request):
        pass
    
    def delete(self, request):
        pass
    
    