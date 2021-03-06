# Generated by Django 3.2.4 on 2021-07-15 20:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CEO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(upload_to='images/')),
                ('Name', models.CharField(max_length=30)),
                ('Rank', models.CharField(max_length=50)),
                ('EntryDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='contactus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=30)),
                ('Email', models.CharField(max_length=50)),
                ('Message', models.CharField(max_length=250)),
                ('EntryDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeePesonalDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FirstName', models.CharField(max_length=30)),
                ('LastName', models.CharField(blank=True, max_length=30)),
                ('CNIC', models.CharField(blank=True, max_length=13, unique=True)),
                ('FatherName', models.CharField(max_length=30)),
                ('Age', models.IntegerField()),
                ('Gender', models.CharField(max_length=8)),
                ('MaritalStatus', models.CharField(max_length=10)),
                ('EntryDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OfferName', models.CharField(max_length=30, unique=True)),
                ('OfferPrice', models.DecimalField(decimal_places=2, max_digits=8)),
                ('Availability', models.CharField(blank=True, max_length=10)),
                ('CreateTime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Req_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='Pending', max_length=255)),
                ('Name_Costomer', models.CharField(max_length=255, null=True)),
                ('GrandTotal', models.FloatField(default='0.00', null=True)),
                ('Address', models.CharField(max_length=255, null=True)),
                ('Phone', models.CharField(max_length=15, null=True)),
                ('EntryDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WebResources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Location', models.CharField(blank=True, max_length=250)),
                ('Phone', models.CharField(blank=True, max_length=13, unique=True)),
                ('Day', models.CharField(blank=True, max_length=10)),
                ('OpeningTime', models.TimeField(blank=True)),
                ('ClosingTime', models.TimeField(blank=True)),
                ('LinkedInLink', models.CharField(blank=True, max_length=100)),
                ('GitLink', models.CharField(blank=True, max_length=100)),
                ('TwitterLink', models.CharField(blank=True, max_length=100)),
                ('FbLink', models.CharField(blank=True, max_length=100)),
                ('EntryDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrdereProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CustomerID', models.IntegerField(null=True)),
                ('Name_Costomer', models.CharField(max_length=255, null=True)),
                ('name', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                ('quantity', models.FloatField()),
                ('EntryDate', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Myapp.req_info')),
            ],
        ),
        migrations.CreateModel(
            name='LoginDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Username', models.CharField(max_length=30)),
                ('Email', models.CharField(max_length=50)),
                ('LoginTime', models.DateTimeField(auto_now=True)),
                ('LoginID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DeliveryAddress', models.CharField(max_length=100)),
                ('ExpectedTime', models.CharField(max_length=10)),
                ('EntryDate', models.DateTimeField(auto_now=True)),
                ('CustomerOrderID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('EmployeePID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Myapp.employeepesonaldetail')),
            ],
        ),
    ]
