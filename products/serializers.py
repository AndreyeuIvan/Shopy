from rest_framework import serializers

from products.models import Product
from shopy.models import Reserved
from shopy.serializers import ReserverSerializer


class ProductSerializer(serializers.ModelSerializer):
    reserve = ReserverSerializer(many=True, required=False)
    price_for_kilo = serializers.ReadOnlyField()
    """
    def validate(self, own_stock, required_qty):
        import pdb;pdb.set_trace()
        if own_stock.number_of_units < required_qty:
            raise serializers.ValidationError('ARRR')
    """

    def create(self, validated_data):
        reserved_data = validated_data.pop("reserve")
        product = Product.objects.create(**validated_data)
        for reserve_data in reserved_data:
            Reserved.objects.create(product=product, **reserve_data)
        return product

    """
    def get_validation_exclusions(self):
        exclusions = super(ProductSerializer, self).get_validation_exclusions()
        return exclusions + ['reserve']
    """

    class Meta:
        model = Product
        fields = ("id", "name", "reserve", "price_for_kilo", "price_for_unit")
        optional_fields = ("reserve",)
