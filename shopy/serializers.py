from rest_framework import serializers
from shopy.models import Reserved, Account, Product

"""
class ReserverSerializer(serializers.ModelSerializer):
    product = serializers.HyperlinkedIdentityField(
        view_name='product-detail'
    )
    product = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    class Meta:
        model = Reserved
        fields = ('user', 'number_of_units', 'product')
"""


class ReserverSerializer(serializers.ModelSerializer):
    """
    product = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )"""

    def validate(self, value_data):
        validated_data = super().validate(value_data)
        print(self.context, "validate")
        # import pdb;pdb.set_trace()
        return validated_data

    def validate_number_of_units(self, data):
        required_qty = self.initial_data["number_of_units"]
        try:
            if self.context["own_stock"] < required_qty:
                raise serializers.ValidationError("ARRR")
        except Exception:
            raise serializers.ValidationError("Except")
        validated_data = super().validate(data)
        return validated_data

    class Meta:
        model = Reserved
        fields = ("number_of_units", "product")


class ProductSerializer(serializers.ModelSerializer):
    reserve = ReserverSerializer(many=True, required=False)
    # import pdb;pdb.set_trace()
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
        fields = ("id", "name", "reserve", "price_for_kilo")
        optional_fields = ("reserve",)


class AccountSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Account
        fields = ("user", "amount")

    def validate(self, data):
        print(data)
        # import pdb;pdb.set_trace()
        # user_amount = Account.objects.get(user=self.context["user"]).amount filter
        if self.context["account_amount"] < self.context["sum_reserved"]:
            raise serializers.ValidationError("Fullfill your account")
        validated_data = super().validate(data)
        return validated_data
