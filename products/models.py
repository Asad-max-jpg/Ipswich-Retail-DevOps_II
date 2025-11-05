from django.db import models
from django.utils.text import slugify
from django.db.models.query import QuerySet


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    inventory = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    # If no image is provided, use a small placeholder so admin/site doesn't show
    # a broken image icon. We set the default at save-time so this change does
    # not require a database migration.
    image = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        """Compatibility shim: accept legacy kwargs 'name' and 'stock'.

        Some tests and earlier code create Product with keywords named
        'name' and 'stock'. The database/migration uses 'title' and
        'inventory'. Map the legacy names to the current field names so
        that both calling styles work without changing the DB schema.
        """
        # map legacy keys to current field names before Model __init__ runs
        if 'name' in kwargs:
            # only set title if it's not already provided
            kwargs.setdefault('title', kwargs.pop('name'))
        if 'stock' in kwargs:
            kwargs.setdefault('inventory', kwargs.pop('stock'))
        super().__init__(*args, **kwargs)

    def clean(self):
        if self.price is not None and self.price < 0:
            raise ValueError("Price cannot be negative")

    def save(self, *args, **kwargs):
        self.clean()
        # Provide a default placeholder image when none is supplied. Doing
        # this here avoids needing a schema migration (no default field
        # change) and ensures both admin-created and programmatically-created
        # products get a valid image URL.
        if not self.image:
            self.image = 'https://placehold.co/400x400/F9F5F2/332C2C?text=No+Image'
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    # Backwards-compatible attribute accessors
    @property
    def stock(self):
        return self.inventory

    @stock.setter
    def stock(self, value):
        self.inventory = value


class ProductQuerySet(QuerySet):
    """QuerySet that understands legacy lookup names ('name' -> 'title', 'stock' -> 'inventory')."""

    def _translate_kwargs(self, kwargs):
        new = {}
        for key, val in kwargs.items():
            parts = key.split('__', 1)
            root = parts[0]
            rest = parts[1] if len(parts) > 1 else ''
            if root == 'name':
                root = 'title'
            elif root == 'stock':
                root = 'inventory'
            new_key = root + ('__' + rest if rest else '')
            new[new_key] = val
        return new

    def filter(self, *args, **kwargs):
        kwargs = self._translate_kwargs(kwargs)
        return super().filter(*args, **kwargs)

    def get(self, *args, **kwargs):
        kwargs = self._translate_kwargs(kwargs)
        return super().get(*args, **kwargs)

    def exclude(self, *args, **kwargs):
        kwargs = self._translate_kwargs(kwargs)
        return super().exclude(*args, **kwargs)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def filter(self, *args, **kwargs):
        return self.get_queryset().filter(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.get_queryset().get(*args, **kwargs)


# Make the custom manager the default so tests that filter by 'name' or
# 'stock' work
Product.add_to_class('objects', ProductManager())
