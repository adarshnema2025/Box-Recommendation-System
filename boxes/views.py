from decimal import Decimal

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Box
from .serializers import RecommendBoxRequestSerializer


class RecommendBoxView(APIView):
    """
    POST /api/recommend-box/

    Given a list of products (with dimensions, weight and quantity),
    recommend the single cheapest box that can hold the whole order.

    Fit rules (as specified in the assignment):
      1. The largest single product (by unit volume) must fit within the
         box's internal dimensions on each axis individually - no rotation.
      2. The combined volume of all products (qty included) must be
         <= the box's internal volume.
      3. The combined weight of all products (qty included) must be
         <= the box's max_weight_capacity.

    Tie-break when multiple boxes qualify: cheapest cost first, then
    smallest internal volume.
    """

    def post(self, request):
        serializer = RecommendBoxRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        products = serializer.validated_data['products']

        total_weight = Decimal('0')
        total_volume = Decimal('0')
        largest_product = None
        largest_product_volume = Decimal('-1')

        for product in products:
            qty = Decimal(product['quantity'])
            unit_volume = product['length'] * product['width'] * product['height']

            total_weight += product['weight'] * qty
            total_volume += unit_volume * qty

            if unit_volume > largest_product_volume:
                largest_product_volume = unit_volume
                largest_product = product

        candidates = []
        for box in Box.objects.all():
            fits_dimensions = (
                largest_product['length'] <= box.internal_length
                and largest_product['width'] <= box.internal_width
                and largest_product['height'] <= box.internal_height
            )
            fits_volume = total_volume <= box.volume
            fits_weight = total_weight <= box.max_weight_capacity

            if fits_dimensions and fits_volume and fits_weight:
                candidates.append(box)

        if not candidates:
            return Response(
                {
                    'recommended_box': None,
                    'message': 'No suitable box found for the given products.',
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Tie-break: cheapest first, then smallest volume.
        candidates.sort(key=lambda b: (b.cost, b.volume))
        best_box = candidates[0]

        return Response(
            {
                'recommended_box': {
                    'serial_no': best_box.serial_no,
                    'name': best_box.name,
                    'internal_length': float(best_box.internal_length),
                    'internal_width': float(best_box.internal_width),
                    'internal_height': float(best_box.internal_height),
                    'max_weight_capacity': float(best_box.max_weight_capacity),
                    'cost': float(best_box.cost),
                },
                'total_weight': float(total_weight),
                'total_volume': float(total_volume),
            },
            status=status.HTTP_200_OK,
        )