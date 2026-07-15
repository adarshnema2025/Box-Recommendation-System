from rest_framework import serializers

from .models import Box


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = (
            'serial_no', 'name', 'internal_length', 'internal_width',
            'internal_height', 'max_weight_capacity', 'cost',
        )


class ProductSerializer(serializers.Serializer):
    """
    A single product line item from the incoming order.

    `quantity` defaults to 1 so a caller can still send a single product
    without quantity for a simple one-item order.
    """
    length = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    width = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    height = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    weight = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    quantity = serializers.IntegerField(min_value=1, default=1)


class RecommendBoxRequestSerializer(serializers.Serializer):
    """
    Expected request body:

    {
        "products": [
            {"length": 20, "width": 15, "height": 10, "weight": 2, "quantity": 3},
            {"length": 12, "width": 12, "height": 12, "weight": 1.5, "quantity": 2}
        ]
    }
    """
    products = ProductSerializer(many=True)

    def validate_products(self, value):
        if not value:
            raise serializers.ValidationError('At least one product is required.')
        return value