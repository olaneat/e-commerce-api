# Generated by Django 4.2 on 2023-05-23 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_manufacturermodel_alter_productmodel_manufacturer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='category', to='products.categorymodel'),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='manufacturer', to='products.manufacturermodel'),
        ),
    ]
