from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.db.models.fields import UUIDField
import jwt
import uuid
from datetime import timedelta, datetime
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse


class CustomManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password=None):
        if email is None:
            raise ValueError('email is required')

        if username is None:
            raise ValueError('username is required')

        email = self.normalize_email(email)
        #user = self.model(email=email, username=username)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        if password is None:
            raise TypeError('password field is required')

        user = self._create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

        '''extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must have is_staff=True')
        if extra_fields.get('is_superuser')is not True:
            raise ValueError('superuser must have is_superuser=True')
        '''


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True,
                          editable=False, default=uuid.uuid4)    
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    password = models.CharField(max_length=100)
    created = models.DateField(auto_now=True)
    timestamp = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=5)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    # @property
    # def token(self):
    #     return self._generate_jwt_token()

    # def _generate_jwt_token(self):
    #     dt = datetime.now() + timedelta(minutes=180)
    #     token = jwt.encode({
    #         'id': self.pk,
    #         'exp': int(dt.strftime('%s'))
    #     }, settings.SECRET_KEY, algorithm='HS256')
    #     return token.decode('utf-8')

    class Meta:
        ordering = ('email',)

    objects = CustomManager()
