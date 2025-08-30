from .models import Orders
from rest_framework import serializers 



class CreateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = [
                'price', 
                'email', 
                'user',
                'created_at',
                'updated_at'
            ]