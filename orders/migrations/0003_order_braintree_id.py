# Generated by Django 3.2.6 on 2021-08-28 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20210826_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='braintree_id',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
