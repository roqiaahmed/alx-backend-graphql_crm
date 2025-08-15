import django
import os

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql_crm.settings")
django.setup()

from crm.models import Customer


def seed():
    customers = [
        Customer(name="John Doe", email="john@example.com", phone="123456789"),
        Customer(name="Jane Doe", email="jane@example.com", phone="987654321"),
    ]
    Customer.objects.bulk_create(customers)
    print("Database seeded successfully!")


if __name__ == "__main__":
    seed()
