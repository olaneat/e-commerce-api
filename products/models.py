from django.db import models
from uuid import uuid4
from register.models import CustomUser
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


# Create your models here.


class CategoryModel(models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True, default=uuid4)
    name = models.CharField(max_length=250, blank=True, null=True )
    img = CloudinaryField('images/category', blank=True, null=True)
    slug  = models.SlugField(max_length=250,  blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: 
        verbose_name  = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name



class ManufacturerModel(models.Model):
    name= models.CharField(max_length=150, blank=True, null=True)
    slug = models.SlugField(unique=True, null=False)
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid4)
    created_on = models.DateTimeField(auto_now_add=True )
    img = CloudinaryField('image/manufacturer')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('-created_on',)
        verbose_name = 'Manufacturer'
        verbose_name_plural = 'Manufacturers'





class ProductModel(models.Model):    
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid4)
    name = models.CharField(max_length=255, blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True, )
    manufacturer = models.ForeignKey(ManufacturerModel, on_delete=models.RESTRICT, related_name='product_manufacturer', blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, blank=True,null=True )
    slug = models.SlugField(max_length=250, blank=True, null=True)
    update_at = models.DateTimeField(auto_now_add=True,)
    category  = models.ForeignKey(CategoryModel, on_delete=models.RESTRICT, related_name='product_category', blank=True, null=True)
    img = CloudinaryField('image', blank=True,null=True)
    available= models.BooleanField(default=True)
    stock = models.IntegerField(default=1)
    model = models.CharField(max_length=255, blank=True,null=True)
    colour= models.CharField(max_length=255, blank=True,null=True)
    weight = models.CharField(max_length=255, blank=True,null=True)
    brand = models.CharField(max_length=255, blank=True,null=True)
    wlan = models.CharField(max_length=255, blank=True,null=True)
    storage = models.CharField(max_length=255, blank=True,null=True)
    rear_camera = models.CharField(max_length=255, blank=True,null=True)
    front_camera = models.CharField(max_length=255, blank=True,null=True)
    connectivity = models.CharField(max_length=255, blank=True,null=True)
    bluetooth = models.CharField(max_length=255, blank=True,null=True)
    size = models.CharField(max_length=255, blank=True,null=True)
    sku = models.CharField(max_length=255, blank=True,null=True)
    line = models.CharField(max_length=255, blank=True,null=True)
    processor = models.CharField(max_length=255, blank=True,null=True)
    display = models.TextField( blank=True,null=True)
    battery = models.CharField(max_length=255, blank=True,null=True)
    platform = models.CharField(max_length=255, blank=True,null=True)
    sim = models.CharField(max_length=255, blank=True,null=True)
    memory = models.CharField(max_length=255, blank=True,null=True)


    class Meta:
        ordering = ('-created_on',)
        index_together = (('id', 'slug'))
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name



# class ReviewModel(models.Model):
from django.db import models
from uuid import uuid4
from register.models import CustomUser
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


# Create your models here.


class CategoryModel(models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True, default=uuid4)
    name = models.CharField(max_length=250, blank=True, null=True )
    img = CloudinaryField('images/category', blank=True, null=True)
    slug  = models.SlugField(max_length=250,  blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: 
        verbose_name  = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name



class ManufacturerModel(models.Model):
    name= models.CharField(max_length=150, blank=True, null=True)
    slug = models.SlugField(unique=True, null=False)
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid4)
    created_on = models.DateTimeField(auto_now_add=True )
    img = CloudinaryField('image/manufacturer')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('-created_on',)
        verbose_name = 'Manufacturer'
        verbose_name_plural = 'Manufacturers'





class ProductModel(models.Model):    
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid4)
    name = models.CharField(max_length=255, blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True, )
    manufacturer = models.ForeignKey(ManufacturerModel, on_delete=models.RESTRICT, related_name='product_manufacturer', blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, blank=True,null=True )
    slug = models.SlugField(max_length=250, blank=True, null=True)
    update_at = models.DateTimeField(auto_now_add=True,)
    category  = models.ForeignKey(CategoryModel, on_delete=models.RESTRICT, related_name='product_category', blank=True, null=True)
    img = CloudinaryField('image', blank=True,null=True)
    available= models.BooleanField(default=True)
    stock = models.IntegerField(default=1)
    model = models.CharField(max_length=255, blank=True,null=True)
    colour= models.JSONField(default=list, blank=True, null=True)
    weight = models.CharField(max_length=255, blank=True,null=True)
    brand = models.CharField(max_length=255, blank=True,null=True)
    wlan = models.CharField(max_length=255, blank=True,null=True)
    storage = models.CharField(max_length=255, blank=True,null=True)
    rear_camera = models.CharField(max_length=255, blank=True,null=True)
    front_camera = models.CharField(max_length=255, blank=True,null=True)
    connectivity = models.CharField(max_length=255, blank=True,null=True)
    bluetooth = models.CharField(max_length=255, blank=True,null=True)
    size = models.JSONField(default=list, blank=True, null=True)
    sku = models.CharField(max_length=255, blank=True,null=True)
    line = models.CharField(max_length=255, blank=True,null=True)
    processor = models.CharField(max_length=255, blank=True,null=True)
    display = models.TextField( blank=True,null=True)
    battery = models.CharField(max_length=255, blank=True,null=True)
    platform = models.CharField(max_length=255, blank=True,null=True)
    sim = models.CharField(max_length=255, blank=True,null=True)
    memory = models.CharField(max_length=255, blank=True,null=True)


    class Meta:
        ordering = ('-created_on',)
        index_together = (('id', 'slug'))
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


    @property
    def image_url(self):
        # Generate the full Cloudinary URL
        return cloudinary.utils.cloudinary_url(self.image.public_id)[0]
# class ReviewModel(models.Model):