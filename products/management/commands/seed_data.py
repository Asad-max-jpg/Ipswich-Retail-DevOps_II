import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Category, Product


class Command(BaseCommand):
    help = "Seed sample fragrance categories and products for PoC"

    def handle(self, *args, **options):
        # Optionally create a default superuser from environment variables.
        # Provide DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, and
        # DJANGO_SUPERUSER_PASSWORD in your deployment environment if you want
        # an automatic admin created on startup. This is idempotent: it will
        # not overwrite an existing user.
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if username and password:
            User = get_user_model()
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, email=email or '', password=password)
                self.stdout.write(self.style.SUCCESS(f"✅ Superuser '{username}' created."))
            else:
                self.stdout.write(self.style.NOTICE(f"Superuser '{username}' already exists; skipping creation."))

        categories = [
            "Floral", "Woody", "Fresh", "Oriental"
        ]
        for cat_name in categories:
            Category.objects.get_or_create(name=cat_name)

        sample_products = [
            {
                "title": "Rose Serenity",
                "price": 75,
                "description": "A romantic fragrance with rose petals, peony and a touch of white musk.",
                "category": "Floral",
                "image": "https://placehold.co/400x400/F9F5F2/332C2C?text=Rose+Serenity"
            },
            {
                "title": "Sandalwood Dusk",
                "price": 85,
                "description": "Smooth sandalwood layered with warm amber and creamy tonka.",
                "category": "Woody",
                "image": "https://placehold.co/400x400/F9F5F2/332C2C?text=Sandalwood+Dusk"
            },
            {
                "title": "Citrus Bloom",
                "price": 65,
                "description": "Bright citrus notes with neroli and bergamot for a fresh, lively scent.",
                "category": "Fresh",
                "image": "https://placehold.co/400x400/F9F5F2/332C2C?text=Citrus+Bloom"
            },
            {
                "title": "Midnight Oud",
                "price": 95,
                "description": "Rich oud, smoky vetiver and dark vanilla for a mysterious allure.",
                "category": "Oriental",
                "image": "https://placehold.co/400x400/F9F5F2/332C2C?text=Midnight+Oud"
            },
            {
                "title": "Vanilla Dream",
                "price": 70,
                "description": "Soft vanilla and jasmine blend for a cozy, comforting fragrance.",
                "category": "Oriental",
                "image": "https://placehold.co/400x400/F9F5F2/332C2C?text=Vanilla+Dream"
            },
            {
                "title": "Aqua Marine",
                "price": 60,
                "description": "Clean ocean breeze and lemon zest with hints of cedarwood.",
                "category": "Fresh",
                "image": "https://placehold.co/400x400/F9F5F2/332C2C?text=Aqua+Marine"
            }
        ]

        for prod in sample_products:
            cat = Category.objects.get(name=prod["category"])
            Product.objects.get_or_create(
                title=prod["title"],
                defaults={
                    "price": prod["price"],
                    "description": prod["description"],
                    "category": cat,
                    "image": prod["image"]
                }
            )
        self.stdout.write(self.style.SUCCESS(
            "✅ Sample fragrance data seeded successfully."))
