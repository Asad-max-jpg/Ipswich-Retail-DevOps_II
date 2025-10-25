from django.db import models
from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    shipped = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.pk} - {self.email}"

    @property
    def products(self):
        """Provide a lightweight products accessor that supports .add(product[, quantity]).

        This is a thin compatibility shim so code/tests that call `order.products.add(product)`
        will create an OrderItem for the order. This avoids changing DB schema and keeps
        behaviour explicit.
        """
        class _ProductsAccessor:
            def __init__(self, order):
                self._order = order

            def add(self, product, quantity=1):
                # create a corresponding OrderItem; price pulled from product
                OrderItem.objects.create(
                    order=self._order,
                    product=product,
                    quantity=quantity,
                    price=getattr(product, 'price', 0)
                )

            # allow simple iteration over related items
            def all(self):
                return [oi.product for oi in self._order.items.all()]

        return _ProductsAccessor(self)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product}"
