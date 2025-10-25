from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from decimal import Decimal
from .models import Order, OrderItem
from products.models import Category, Product

User = get_user_model()


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            title="Test Product",
            description="Test Description",
            price=Decimal("99.99"),
            inventory=10,
            category=self.category
        )
        self.order = Order.objects.create(
            user=self.user,
            email='test@example.com'
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=Decimal("99.99")
        )

    def test_order_creation(self):
        """Ensure order is created and linked to user correctly."""
        self.assertEqual(self.order.email, 'test@example.com')
        self.assertEqual(self.order.user, self.user)
        self.assertFalse(self.order.shipped)
        self.assertTrue(isinstance(self.order, Order))
        self.assertEqual(str(self.order),
                         f"Order {self.order.pk} - test@example.com")

    def test_order_item_creation(self):
        """Ensure order items store correct quantity and product link."""
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.price, Decimal("99.99"))
        self.assertEqual(str(self.order_item), "2 x Test Product")

    def test_total_calculation(self):
        """Ensure total amount can be calculated correctly."""
        total = self.order_item.quantity * self.order_item.price
        self.assertEqual(total, Decimal("199.98"))


class OrderViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            title="Test Product",
            description="Test Description",
            price=Decimal("99.99"),
            inventory=10,
            category=self.category
        )

    def test_order_creation_authenticated(self):
        """Ensure logged-in user can create an order."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('orders:create'), {
            'email': 'test@example.com',
            'items': [{'product_id': self.product.id, 'quantity': 1}]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Order.objects.exists())

    def test_order_creation_unauthenticated(self):
        """Ensure unauthenticated users are redirected to login page."""
        response = self.client.post(reverse('orders:create'), {
            'email': 'anon@example.com',
            'items': [{'product_id': self.product.id, 'quantity': 1}]
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_order_list_view_authenticated(self):
        """Ensure authenticated users can access their orders page."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('orders:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_list.html')

    def test_order_flow_integration(self):
        """Full integration test: product → order → order item creation."""
        self.client.login(username='testuser', password='testpass123')
        order = Order.objects.create(user=self.user, email='test@example.com')
        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=3,
            price=self.product.price)
        response = self.client.get(reverse('orders:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")
        self.assertContains(response, "99.99")
