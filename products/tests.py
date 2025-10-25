from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from .models import Category, Product
from django.db.utils import IntegrityError


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")

    def test_category_creation(self):
        """Ensure category is created with proper slug and string representation."""
        self.assertEqual(self.category.name, "Electronics")
        self.assertEqual(self.category.slug, "electronics")
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(str(self.category), "Electronics")

    def test_category_slug_generation(self):
        """Ensure category slug is auto-generated correctly."""
        category = Category.objects.create(name="Home & Garden")
        self.assertEqual(category.slug, "home-garden")

    def test_duplicate_category_name(self):
        """Creating a category with duplicate name should raise IntegrityError if slug is unique."""
        Category.objects.create(name="Perfumes")
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Perfumes")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            title="Test Product",
            description="Test Description",
            price=Decimal("99.99"),
            inventory=10,
            category=self.category
        )

    def test_product_creation(self):
        """Ensure product is created correctly and slug is generated."""
        self.assertEqual(self.product.title, "Test Product")
        self.assertEqual(self.product.slug, "test-product")
        self.assertEqual(self.product.price, Decimal("99.99"))
        self.assertEqual(self.product.inventory, 10)
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(str(self.product), "Test Product")

    def test_product_slug_generation(self):
        """Ensure product slug correctly removes symbols and spaces."""
        product = Product.objects.create(
            title="New & Exciting Product",
            price=Decimal("199.99"),
            inventory=5,
            category=self.category
        )
        self.assertEqual(product.slug, "new-exciting-product")

    def test_invalid_price_raises_error(self):
        """Ensure product with negative price raises ValueError."""
        with self.assertRaises(ValueError):
            Product.objects.create(
                title="Invalid Product",
                price=Decimal("-10.00"),
                inventory=5,
                category=self.category
            )


class ProductViewsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            title="Test Product",
            description="Test Description",
            price=Decimal("99.99"),
            inventory=10,
            category=self.category
        )

    def test_product_list_view(self):
        """Ensure product list view renders correctly and shows product."""
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")
        self.assertTemplateUsed(response, "products/product_list.html")

    def test_product_detail_view(self):
        """Ensure product detail page loads and displays product info."""
        response = self.client.get(
            reverse(
                'products:detail', kwargs={
                    'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")
        self.assertContains(response, "99.99")
        self.assertTemplateUsed(response, "products/product_detail.html")

    def test_non_existent_product_returns_404(self):
        """Ensure accessing non-existent product returns 404."""
        response = self.client.get(
            reverse(
                'products:detail', kwargs={
                    'slug': 'fake-product'}))
        self.assertEqual(response.status_code, 404)
