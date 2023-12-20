import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from webapp.models import NetworkNode, EmployeeProfileInfo, Contact, Address, Product
from faker import Faker


def create_admin(handle):

    username = "admin"
    email = "admin@gmail.com"
    password = "adminpas"

    # Try to get the superuser, or create it if it doesn't exist
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email, 'is_staff': True, 'is_superuser': True}
    )

    if created:
        # Set the password for the new superuser
        user.set_password(password)
        user.save()
        handle.stdout.write(handle.style.SUCCESS('Superuser created successfully'))


def getf_fake_address(fake):
    country = fake.country()
    city = fake.city()
    street = fake.street_name()
    house_number = fake.building_number()

    return Address.objects.create(
        country=country,
        city=city,
        street=street,
        house_number=house_number
    )


def get_fake_contact(fake):
    email = fake.email()
    address = getf_fake_address(fake)

    return Contact.objects.create(
        email=email,
        address=address
    )


def get_fake_products(fake, count=5):
    products = []

    for _ in range(random.randint(1, count)):
        product = Product(
            name=fake.word(),
            model=fake.word(),
            release_date=fake.date_this_decade(),
        )
        products.append(product)

    with transaction.atomic():
        Product.objects.bulk_create(products)

    return products


def get_fake_employees(fake, count=5):
    employees = []

    for _ in range(count):
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        employee = EmployeeProfileInfo.objects.get(user_id=user.id)
        employee.address = fake.address()
        employee.birth_date = fake.date_of_birth()
        employee.position = fake.random_element(elements=EmployeeProfileInfo.Position.values)
        employee.save()
        employees.append(employee)

    return employees


class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **options):

        create_admin(self)

        fake = Faker()

        for _ in range(10):
            try:

                supplier = None
                contact = get_fake_contact(fake)
                products = get_fake_products(fake)
                employees = get_fake_employees(fake)


                network_node = NetworkNode.objects.create(
                    name=fake.company(),
                    supplier=None,
                    contact=contact,
                    created_at=fake.date_time_this_decade(tzinfo=timezone.utc),
                    debt=fake.pydecimal(left_digits=4, right_digits=2, positive=True),
                )
                network_node.employees.set(employees)
                network_node.products.set(products)

                existing_nodes = NetworkNode.objects.filter(network_level__lt=3)
                random_supplier = random.choice(existing_nodes)
                network_node.supplier = random_supplier
                network_node.network_level = random.randint(random_supplier.network_level, 4)
                network_node.save()

                self.stdout.write(self.style.SUCCESS(f'Successfully created NetworkNode: {network_node}'))

            except Exception as e:
                continue

        self.stdout.write(self.style.SUCCESS('Database population complete'))

