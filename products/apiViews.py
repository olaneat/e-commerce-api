from rest_framework import generics
from .serializers import (CategorySerializer, 
                          CreateProductSerializer, 
                          ListProductListSerializer, 
                          CreateCategorySerializer
                        )
from .models import ProductModel, CategoryModel
from rest_framework import permissions

class CreateProductAPIView(generics.CreateAPIView):
    lookup_field = 'id'
    serializer_class = CreateProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ProductModel.objects.all()



class ListProductAPIView(generics.ListAPIView):
    lookup_field = 'id'
    serializer_class = ListProductListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = ProductModel.objects.all()



class ProductDetailAPIView(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ProductModel.objects.all()
    
    

class UpdateProductAPIView(generics.UpdateAPIView):
    lookup_field = 'id'
    serializer_class = CreateProductSerializer
    permission_classes = [permissions.IsAdminUser]
    def get_queryset(self, id):
        queryset = ProductModel.objects.get(id=id)
        return queryset
   
class DeleteProductAPIView(generics.DestroyAPIView):
    lookup_field = 'id'
    serializer_class = CreateProductSerializer
    permission_classes = [permissions.IsAdminUser]
    def get_queryset(self, id):
        queryset = ProductModel.objects.get(id=id)
        return queryset

class CreateCatogoeryAPIView(generics.CreateAPIView):
    lookup_field = 'id'
    serializer_class = CreateCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CategoryModel.objects.all()


class UpdateCategoryAPIView(generics.UpdateAPIView):
    lookup_field = 'id'
    serializer_class = CategoryModel
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
         queryset = CategoryModel.object.get(id=self.id)
         return queryset
    

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