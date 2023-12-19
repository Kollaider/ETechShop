# Generated by Django 3.2 on 2023-12-19 14:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0003_auto_20231219_1311'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactinfo',
            options={'ordering': ['email']},
        ),
        migrations.AlterModelOptions(
            name='networknode',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['release_date']},
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(help_text='City', max_length=100),
        ),
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(help_text='Country', max_length=100),
        ),
        migrations.AlterField(
            model_name='address',
            name='house_number',
            field=models.CharField(help_text='House number', max_length=10),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(help_text='Street', max_length=100),
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='address',
            field=models.OneToOneField(help_text='Address associated with the contact information', on_delete=django.db.models.deletion.CASCADE, to='webapp.address'),
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='email',
            field=models.EmailField(help_text='Email address', max_length=254),
        ),
        migrations.AlterField(
            model_name='employeeprofileinfo',
            name='address',
            field=models.TextField(blank=True, help_text="Employee's address", max_length=500),
        ),
        migrations.AlterField(
            model_name='employeeprofileinfo',
            name='birth_date',
            field=models.DateField(blank=True, help_text="Employee's birth date", null=True),
        ),
        migrations.AlterField(
            model_name='employeeprofileinfo',
            name='position',
            field=models.CharField(choices=[('Manager', 'Manager'), ('Consultant', 'Consultant'), ('Seller', 'Seller'), ('Employee', 'Employee')], default='Employee', help_text="Employee's position in the company", max_length=20),
        ),
        migrations.AlterField(
            model_name='employeeprofileinfo',
            name='user',
            field=models.OneToOneField(help_text='Reference to the user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='networknode',
            name='contacts',
            field=models.ManyToManyField(blank=True, help_text='Contact information for the network node', related_name='network_nodes', to='webapp.ContactInfo'),
        ),
        migrations.AlterField(
            model_name='networknode',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Date and time of node creation'),
        ),
        migrations.AlterField(
            model_name='networknode',
            name='debt',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Debt amount for the network node', max_digits=10),
        ),
        migrations.AlterField(
            model_name='networknode',
            name='employees',
            field=models.ManyToManyField(blank=True, help_text='Employees associated with the network node', related_name='network_nodes', to='webapp.EmployeeProfileInfo'),
        ),
        migrations.AlterField(
            model_name='networknode',
            name='name',
            field=models.CharField(help_text='Name of the network node', max_length=100),
        ),
        migrations.AlterField(
            model_name='networknode',
            name='network_level',
            field=models.IntegerField(choices=[(0, 'Factory'), (1, 'Distributor'), (2, 'Dealer Center'), (3, 'Retail Chain'), (4, 'Entrepreneur')], default=0, help_text='Level of the network node'),
        ),
        migrations.AlterField(
            model_name='networknode',
            name='products',
            field=models.ManyToManyField(blank=True, help_text='Products associated with the network node', related_name='nodes', to='webapp.Product'),
        ),
        migrations.AlterField(
            model_name='networknode',
            name='supplier',
            field=models.ForeignKey(blank=True, help_text='Supplier of the network node', null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.networknode'),
        ),
        migrations.AlterField(
            model_name='product',
            name='model',
            field=models.CharField(help_text='Model of the product', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(help_text='Name of the product', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='release_date',
            field=models.DateField(help_text='Date when the product was released'),
        ),
    ]
