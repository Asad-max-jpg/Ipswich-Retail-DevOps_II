from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product


class ProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            title="Dental Mirror",
            description="High-quality mirror for dental use",
            price=5.0,
            inventory=30
        )

    def test_product_list_view(self):
        """Ensure the product list page loads correctly"""
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dental Mirror")

    def test_product_detail_view(self):
        """Ensure product detail page displays correct information"""
        response = self.client.get(
            reverse(
                'products:detail', args=[
                    self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.title)
