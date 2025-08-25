from django.db import migrations
import os
from django.contrib.auth import get_user_model

def create_superuser(apps, schema_editor):
    User = get_user_model()
    username = os.environ.get('SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('SUPERUSER_PASSWORD', 'your_secure_password')
    User.objects.filter(username=username).delete()
    User.objects.create_superuser(username, email, password)

class Migration(migrations.Migration):
    dependencies = [
        ('commerce', '0001_initial'),  # Adjust to your last migration
    ]
    operations = [
        migrations.RunPython(create_superuser),
    ]