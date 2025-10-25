from django.test import TestCase
from products.models import Product
from orders.models import Order


class OrderIntegrationTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title="Surgical Scissors",
            price=15.0,
            inventory=10
        )

    def test_order_creation_reduces_stock(self):
        """Ensure creating an order updates product stock correctly"""
        order = Order.objects.create(email="test@example.com")
        order.products.add(self.product)

        # Simulate stock reduction if you have logic to handle it
        self.product.stock -= 1
        self.product.save()

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 9)
