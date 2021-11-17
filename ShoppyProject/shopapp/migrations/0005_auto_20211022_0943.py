# Generated by Django 2.2.14 on 2021-10-22 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0004_orderitemmodel_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaddressmodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shopapp.UserProfileRegistrationModel'),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='billingAddress',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billingAddress', to='shopapp.BillingAddressModel'),
        ),
    ]
