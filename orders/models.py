from django.db import models
import uuid
from register.models import CustomUser

# Create your models here.

class Orders(models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True, default=uuid.uuid4)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField(max_length=254)
    reference = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Orders"
        
    def __str__(self):
        return str(self.reference)

    def generate_number(self):
        self.reference = random.randint(10000, 99999)
        self.save()

    