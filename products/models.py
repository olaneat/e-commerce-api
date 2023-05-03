from django.db import models
from uuid import uuid4
from register.models import CustomUser
from cloudinary.models import CloudinaryField
# Create your models here.


class CategoryModel(models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True, default=uuid4)
    name = models.CharField(max_length=250 )
    slug  = models.SlugField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: 
        verbose_name  = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name
    

class ProductModel(models.Model):    
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, )
    price = models.DecimalField(decimal_places=3, max_digits=10 )
    slug = models.SlugField(max_length=250, blank=True, null=True)
    update_at = models.DateTimeField(auto_now_add=True,)
    category  = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='category', blank=True, null=True)
    img = CloudinaryField('image')
    available= models.BooleanField(default=True)
    stock = models.IntegerField(default=1)

    class Meta:
        ordering = ('-created_on',)
        index_together = (('id', 'slug'))
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    