from rest_framework import serializers 
from .models import ProductModel, CategoryModel, ManufacturerModel



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
                'price',         
                'id',
                'maunfacuturer'    
            ]

    
    

class ListProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = ProductModel
        fields = ['name', 'id', 'category', 'price', 'img']

    

class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__' 



class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)


    def create(self, validated_data):
        print(validated_data)
        goods =validated_data.pop('products')
        category = CategoryModel.objects.create(**validated_data)
        for product in goods:
            ProductModel.objects.create(category=category, product=product)
        return category


    class Meta: 
        model = CategoryModel
        fields  = [ 'name', 'slug', 'products', 'id']

class ListManufactuererSerializer(serializers.ModelSerializer):
    products = serializers.SlugRelatedField(many=True, slug_field='name',read_only=True )

    def create(self, validated_data):
        print(validated_data)
        goods = validated_data.pop('products')
        manufacturer = ManufacturerModel.objects.create(**validated_data)
        for product in goods:
            ProductModel.objects.create(manufacturer=manufacturer, product=product)
        return manufacturer
    
    class Meta:
        model = ManufacturerModel
        fields = ['id', 'name', 'slug', 'img', 'products']


class CreateManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManufacturerModel
        fields = '__all__'



    '''
    def create(self, validated_data):
        if 'category' in validated_data:
            products =validated_data.pop('category')
        category = CategoryModel.objects.create(**validated_data)
        for product in products:
            ProductModel.objects.create(category=category, product=product)
        return category
    '''
