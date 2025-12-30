from rest_framework import serializers 
from .models import ProductModel, CategoryModel, ManufacturerModel



class CreateProductSerializer(serializers.ModelSerializer):
    # size = serializers.ListField(
    #     child=serializers.CharField(max_length=20),
    #     allow_empty=True,
    #     required=False
    # )
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
                'manufacturer',
                'model',
                'colour',
                'weight',
                'brand',
                'wlan',
                'storage',
                'connectivity',
                'display',
                'battery',
                'platform',
                'processor',
                'front_camera',
                'rear_camera',
                'sku',
                'line',
                'size',
                'sim',
                'bluetooth',
                'memory'
            ]

    
class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    manufacturer = serializers.CharField(source='manufacturer.name', read_only=True)
    manufacturer_id = serializers.CharField(source='manufacturer.id', read_only=True)
    
    class Meta:
        model = ProductModel
        fields = [
                'name', 
                'description', 
                'img',
                'slug',
                'manufacturer_id', 
                'available',
                'stock', 
                'category',
                'price',         
                'id',
                'manufacturer',
                'model',
                'colour',
                'weight',
                'brand',
                'wlan',
                'storage',
                'connectivity',
                'display',
                'memory',
                'battery',
                'platform',
                'processor',
                'front_camera',
                'rear_camera',
                'sku',
                'line',
                'size',
                'sim',
                'bluetooth'
            ]
    
    

class ListProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = ProductModel
        fields = ['name', 'id', 'category', 'price', 'img']
    

class CreateCategorySerializer(serializers.ModelSerializer):
    # product_category = serializers.StringRelatedField(many=True)
    class Meta:
        model = CategoryModel
        fields = ['name', 'slug', 'img']

    # def create(self, validated_data):
    #     print(validated_data)
    #     product_data = validated_data.pop('product_category')
    #     category = CategoryModel.objects.create(**validated_data)
    #     for product in product_data:
    #         ProductModel.objects.create(category=category, **validated_data)
    #     return category

class CategorySerializer(serializers.ModelSerializer):
    #cat = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)    

    class Meta: 
        model = CategoryModel
        fields  = [ 'name', 'slug', 'id', 'img']

class ListManufactuererSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ManufacturerModel
        fields = ['id', 'name', 'slug', 'img']


class ManufacturerDetailSerializer(serializers.ModelSerializer):
    product_manufacturer = serializers.StringRelatedField(many=True )
    class Meta:
        model = ManufacturerModel
        fields = ['id', 'name', 'slug', 'img', 'product_manufacturer']


class CreateManufacturerSerializer(serializers.ModelSerializer):
    product_manufacturer = serializers.StringRelatedField(many=True )
    
    class Meta:
        model = ManufacturerModel
        fields = '__all__'


    def create(self, validated_data):
        product_data = validated_data.pop('product_manufacturer')
        manufacturer = ManufacturerModel.objects.create(**validated_data)
        for product in product_data:
            ProductModel.objects.create(manufacturer=manufacturer, **validated_data)
        return manufacturer



    '''
    def create(self, validated_data):
        if 'category' in validated_data:
            products =validated_data.pop('category')
        category = CategoryModel.objects.create(**validated_data)
        for product in products:
            ProductModel.objects.create(category=category, product=product)
        return category
    '''



class SearchSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=200)
    name = serializers.CharField(max_length=200)
    type = serializers.CharField(max_length=20)