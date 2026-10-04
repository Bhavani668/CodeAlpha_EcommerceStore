from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = "Create sample products"

    def handle(self, *args, **kwargs):
        products = [
            ("Wireless Headphones", "Clear sound and comfortable design.", "1499", 20),
            ("Smart Watch", "Fitness and notification smartwatch.", "2499", 15),
            ("Running Shoes", "Lightweight shoes for everyday running.", "1999", 25),
            ("College Backpack", "Durable backpack for college and travel.", "999", 30),
        ]
        for name, desc, price, stock in products:
            Product.objects.update_or_create(
                name=name,
                defaults={"description": desc, "price": price, "stock": stock}
            )
        self.stdout.write(self.style.SUCCESS("Sample products added."))
