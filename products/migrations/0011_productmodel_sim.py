# Generated by Django 4.2 on 2023-06-24 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_rename_ram_productmodel_bluetooth_productmodel_wlan'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='sim',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]