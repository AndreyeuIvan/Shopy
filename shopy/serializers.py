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


class ReserverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reserved
        fields = ('user', 'number_of_units', 'product')


class ProductSerializer(serializers.ModelSerializer):
    reverse = ReserverSerializer(many=True)

    def create(self, validated_data):

        reverses_data = validated_data.pop('reverse')
        product = Product.objects.create(**validated_data)
        for reverse_data in reverses_data:
            Reserved.objects.create(product=product, **reverse_data)
        return product

    class Meta:
        model = Product
        fields = ('id', 'name')


class AccountSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Account
        fields = ('user', 'amount')
