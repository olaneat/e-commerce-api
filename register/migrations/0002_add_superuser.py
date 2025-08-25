from django.db import migrations
import os
from django.contrib.auth import get_user_model

def create_superuser(apps, schema_editor):
    User = get_user_model()
    email = os.environ.get('SUPERUSER_EMAIL', 'admin@abc.com')
    username = os.environ.get('SUPERUSER_USERNAME', 'admin')
    password = os.environ.get('SUPERUSER_PASSWORD', 'password')
    role = os.environ.get('SUPERUSER_ROLE', 'admin')
    print(f"DEBUG: Creating superuser with email={email}, username={username}, role={role}, password=***")
    try:
        User.objects.filter(email=email).delete()
        User.objects.create_superuser(
            email=email,
            username=username,
            password=password,
            role=role
        )
        print(f"DEBUG: Superuser {email} created successfully")
    except Exception as e:
        print(f"DEBUG: Superuser creation failed: {str(e)}")

class Migration(migrations.Migration):
    dependencies = [
        ('commerce', '0001_initial'),  # Depends on your user model migration
    ]
    operations = [
        migrations.RunPython(create_superuser),
    ]