# Generated by Django 4.2 on 2023-06-21 22:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_productmodel_specifications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productmodel',
            name='specifications',
        ),
        migrations.AddField(
            model_name='productspecificationmodel',
            name='product',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product', to='products.productmodel'),
        ),
    ]
