from django.contrib.auth.models import AbstractUser, User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class EmployeeProfileInfo(models.Model):
    """
    Model representing employee profile information.
    """

    class Position(models.TextChoices):
        MANAGER = 'Manager'
        CONSULTANT = 'Consultant'
        SELLER = 'Seller'
        EMPLOYEE = 'Employee'

    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text="Reference to the user")
    address = models.TextField(max_length=500, blank=True, help_text="Employee's address")
    birth_date = models.DateField(null=True, blank=True, help_text="Employee's birth date")
    position = models.CharField(
        max_length=20,
        choices=Position.choices,
        default=Position.EMPLOYEE,
        help_text="Employee's position in the company",
    )

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Product(models.Model):
    """
    Model representing a product.
    """

    name = models.CharField(max_length=100, help_text="Name of the product")
    model = models.CharField(max_length=100, help_text="Model of the product")
    release_date = models.DateField(help_text="Date when the product was released")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['release_date']  # Order products by release date by default



class NetworkNode(models.Model):
    """
    Model representing a network node in the electronic sales network.
    """
    class NetworkLevel(models.IntegerChoices):
        FACTORY = 0
        DISTRIBUTOR = 1
        DEALER_CENTER = 2
        RETAIL_CHAIN = 3
        ENTREPRENEUR = 4

    name = models.CharField(max_length=100, help_text="Name of the network node")
    network_level = models.IntegerField(
        choices=NetworkLevel.choices,
        default=NetworkLevel.FACTORY,
        help_text="Level of the network node"
    )
    hierarchy_level = models.IntegerField()
    supplier = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Supplier of the network node"
    )
    contact = models.OneToOneField(
        'Contact',
        related_name='network_node',
        null=True,
        blank=True,
        help_text="Contact information for the network node",
        on_delete=models.CASCADE,
    )
    products = models.ManyToManyField(
        'Product',
        related_name='nodes',
        help_text="Products associated with the network node",
        blank=True,
    )
    debt = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Debt amount for the network node"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="Date and time of node creation"
    )
    employees = models.ManyToManyField(
        'EmployeeProfileInfo',
        related_name='network_nodes',
        blank=True,
        help_text="Employees associated with the network node"
    )

    def __str__(self):
        return f'{self.name} ({self.network_level})'

    def get_level(self):
        level = 0
        node = self
        while node.supplier:
            if node.supplier == self:
                raise ValidationError("Recursive supplier-child relationship is not allowed.")
            level += 1
            node = node.supplier
        return level

    def clean(self):
        if self.supplier:
            if self.network_level <= self.supplier.network_level:
                raise ValidationError("Network level must be higher than the supplier's network level.")

            if self.debt < 0:
                raise ValidationError("Debt amount must be a positive number.")

    def save(self, *args, **kwargs):
        self.hierarchy_level = self.get_level()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['created_at']  # Order network nodes by creation date by default


class Address(models.Model):
    """
    Model representing an address.
    """
    country = models.CharField(max_length=100, help_text="Country")
    city = models.CharField(max_length=100, help_text="City")
    street = models.CharField(max_length=100, help_text="Street")
    house_number = models.CharField(max_length=10, help_text="House number")

    def __str__(self):
        return f"{self.country}, {self.city}, {self.street}, {self.house_number}"


class Contact(models.Model):
    """
    Model representing contact information.
    """
    email = models.EmailField(help_text="Email address")
    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        help_text="Address associated with the contact information"
    )

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['email']  # Order contact info by email address by default

