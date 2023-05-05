from rest_framework import serializers 
from .models import ProductModel, CategoryModel



class CreateProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductModel
        fields = [
                'name', 
                'description', 
                'img',
                'slug', 
                'available',
                'stock', 
                'category',
                'price'         
            ]

    
    

class ListProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = ProductModel
        fields = '__all__'

    

class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__' 



class CategorySerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)


    def create(self, validated_data):
        products =validated_data.pop('category')
        category = CategoryModel.objects.create(**validated_data)
        for product in products:
            ProductModel.objects.create(category=category, product=product)
        return category


    class Meta: 
        model = CategoryModel
        fields  = [ 'name', 'slug', 'category', 'id']


    '''
    def create(self, validated_data):
        if 'category' in validated_data:
            products =validated_data.pop('category')
        category = CategoryModel.objects.create(**validated_data)
        for product in products:
            ProductModel.objects.create(category=category, product=product)
        return category
    '''