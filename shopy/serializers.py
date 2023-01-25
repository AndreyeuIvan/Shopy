from rest_framework import serializers
from shopy.models import Reserved, Account, Product

'''
class ReserverSerializer(serializers.ModelSerializer):
    product = serializers.HyperlinkedIdentityField(
        view_name='product-detail'
    )

    class Meta:
        model = Reserved
        fields = ('user', 'number_of_units', 'product')
'''

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'shop_name', 'unit', 'number_of_units', 'price_for_unit', 'price_for_kg')


class ProductApplySerializer(ProductSerializer):
    id = serializers.IntegerField()



class ReserverSerializer(serializers.ModelSerializer):
    product = ProductApplySerializer()

    class Meta:
        model = Reserved
        fields = ('user', 'number_of_units', 'product')



class AccountSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Account
        fields = ('user', 'amount')
