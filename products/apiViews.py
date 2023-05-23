from rest_framework import generics
from .serializers import (CategorySerializer, 
                          CreateProductSerializer, 
                          ListProductSerializer, 
                          CreateCategorySerializer,
                          ListManufacturerSerializer,
                          CreateManufactuererSerializer
                        )
from .models import ProductModel, CategoryModel, ManufacturerModel
from rest_framework import permissions

class CreateProductAPIView(generics.CreateAPIView):
    lookup_field = 'id'
    serializer_class = CreateProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ProductModel.objects.all()



class ListProductAPIView(generics.ListAPIView):
    lookup_field = 'id'
    serializer_class = ListProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = ProductModel.objects.all()



class ProductDetailAPIView(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = CreateProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = ProductModel.objects.all()
    
    
class UpdateProductAPIView(generics.UpdateAPIView):
    lookup_field = 'id'
    serializer_class = CreateProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ProductModel.objects.all()
    
class DeleteProductAPIView(generics.DestroyAPIView):
    lookup_field = 'id'
    serializer_class = CreateProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ProductModel.objects.all()
    

class CreateCatogoeryAPIView(generics.CreateAPIView):
    lookup_field = 'id'
    serializer_class = CreateCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CategoryModel.objects.all()


class UpdateCategoryAPIView(generics.UpdateAPIView):
    lookup_field = 'id'
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CategoryModel.objects.all()
    

class CategoryListAPIView(generics.ListAPIView):
    lookup_field = 'id'
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = CategoryModel.objects.all()

class DeleteCategoryAPIView(generics.DestroyAPIView):
    lookup_field = 'id'
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = CategoryModel.objects.all()


class CreateManufacturerAPIView(generics.CreateAPIView):
    lookup_field = 'id'
    serializer_class = CreateManufactuererSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ManufacturerModel.objects.all()


class UpdateManufacturerAPIView(generics.UpdateAPIView):
    lookup_field = 'id'
    serializer_class = CreateManufactuererSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ManufacturerModel.objects.all()
    

class ManufacturerListAPIView(generics.ListAPIView):
    lookup_field = 'id'
    serializer_class = ListManufacturerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = ManufacturerModel.objects.all()

class DeleteManufacturerAPIView(generics.DestroyAPIView):
    lookup_field = 'id'
    serializer_class = ListManufacturerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = ManufacturerModel.objects.all()