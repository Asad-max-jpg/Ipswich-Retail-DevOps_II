from django.test import TestCase
from products.models import Product


class ProductIntegrationTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title="Scalpel",
            description="Surgical stainless steel scalpel",
            price=10.0,
            inventory=20
        )

    def test_product_creation_and_retrieval(self):
        """Ensure product is saved and retrievable from DB"""
        product = Product.objects.get(title="Scalpel")
        self.assertEqual(product.price, 10.0)
        self.assertEqual(product.inventory, 20)

    def test_product_stock_update(self):
        """Ensure product stock updates correctly"""
        self.product.inventory -= 5
        self.product.save()
        updated = Product.objects.get(pk=self.product.pk)
        self.assertEqual(updated.inventory, 15)
