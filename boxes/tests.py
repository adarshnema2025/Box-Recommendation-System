from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RecommendBoxTests(APITestCase):
    fixtures = ['boxes.json']

    def setUp(self):
        self.url = reverse('recommend-box')

    def test_success_returns_cheapest_fitting_box(self):
        """
        A single product 20x15x14, weight 5.5 -> total_volume 4200, total_weight 5.5.
        BOX-003 (20x20x20, cap 5) fails on weight.
        BOX-004 (30x25x20, cap 8, cost 40) fits and is the cheapest fitting box.
        BOX-006 also fits but costs more, so it must NOT be chosen.
        """
        payload = {
            'products': [
                {'length': 20, 'width': 15, 'height': 14, 'weight': 5.5, 'quantity': 1}
            ]
        }
        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['recommended_box']['serial_no'], 'BOX-004')
        self.assertEqual(data['total_weight'], 5.5)
        self.assertEqual(data['total_volume'], 4200.0)

    def test_multiple_products_with_quantity_are_aggregated(self):
        """
        3 units of a 10x10x10/1kg product => total_volume 3000, total_weight 3.
        Largest single product (10x10x10) fits in BOX-001 (10x10x10) on every
        axis, but BOX-001's volume (1000) and weight cap (1) are too small,
        so the API must fall through to a bigger box.
        """
        payload = {
            'products': [
                {'length': 10, 'width': 10, 'height': 10, 'weight': 1, 'quantity': 3}
            ]
        }
        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['total_volume'], 3000.0)
        self.assertEqual(data['total_weight'], 3.0)
        # Must not pick BOX-001 (too small), should pick the cheapest box
        # whose volume/weight capacity can hold the aggregated total.
        self.assertNotEqual(data['recommended_box']['serial_no'], 'BOX-001')

    def test_tie_break_prefers_cheaper_then_smaller_volume(self):
        """
        A tiny, light product should fit many boxes; the cheapest
        (BOX-001, cost 15) must be returned.
        """
        payload = {
            'products': [
                {'length': 5, 'width': 5, 'height': 5, 'weight': 0.5, 'quantity': 1}
            ]
        }
        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['recommended_box']['serial_no'], 'BOX-001')

    def test_no_box_fits_returns_404(self):
        """A product larger than every box's largest dimension must return 404."""
        payload = {
            'products': [
                {'length': 200, 'width': 200, 'height': 200, 'weight': 5, 'quantity': 1}
            ]
        }
        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.json()
        self.assertIsNone(data['recommended_box'])
        self.assertIn('message', data)

    def test_overweight_order_returns_404(self):
        """Total weight exceeding every box's capacity must return 404."""
        payload = {
            'products': [
                {'length': 5, 'width': 5, 'height': 5, 'weight': 40, 'quantity': 1}
            ]
        }
        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNone(response.json()['recommended_box'])

    def test_missing_products_returns_400(self):
        response = self.client.post(self.url, {'products': []}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_payload_returns_400(self):
        payload = {
            'products': [
                {'length': -5, 'width': 5, 'height': 5, 'weight': 1, 'quantity': 1}
            ]
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_products_key_returns_400(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)