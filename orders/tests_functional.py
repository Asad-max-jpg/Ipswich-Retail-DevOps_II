from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from orders.models import Order


class OrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='john', password='pass1234')
        self.client.login(username='john', password='pass1234')

    def test_order_list_view_authenticated(self):
        """Ensure logged-in users can access their order list"""
        response = self.client.get(reverse('orders:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Orders")

    def test_order_create_view_post(self):
        """Ensure order creation works via POST"""
        response = self.client.post(
            reverse('orders:create'), {
                'email': 'john@example.com'})
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(
            Order.objects.filter(
                email='john@example.com').exists())
