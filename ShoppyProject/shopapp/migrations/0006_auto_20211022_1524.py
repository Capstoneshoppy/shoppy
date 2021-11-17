# Generated by Django 2.2.14 on 2021-10-22 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0005_auto_20211022_0943'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingAdress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_type', models.CharField(blank=True, max_length=15, null=True)),
                ('completeStreetAddress', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(max_length=20, null=True)),
                ('state', models.CharField(max_length=20, null=True)),
                ('zipcode', models.IntegerField(null=True)),
                ('country', models.CharField(max_length=20)),
                ('orderId', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shopapp.UserProfileRegistrationModel')),
            ],
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='shippingAddress',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shippingAddress', to='shopapp.ShippingAdress'),
        ),
        migrations.DeleteModel(
            name='AddressModel',
        ),
    ]
