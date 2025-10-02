from rest_framework import generics
from .serializers import (
    CategorySerializer, 
    ListProductSerializer, 
    CreateCategorySerializer,
    CreateManufacturerSerializer,
    ListManufactuererSerializer,                     
    CreateProductSerializer, 
    ProductDetailSerializer,
    SearchSerializer,
    ManufacturerDetailSerializer,
    )

from rest_framework.views import APIView
from .models import ProductModel, CategoryModel, ManufacturerModel
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import Response
from rest_framework import status
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

class CreateProductAPIView(generics.CreateAPIView):
    lookup_field = 'id'
    serializer_class = CreateProductSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = ProductModel.objects.all()

class ListProductAPIView(generics.ListAPIView):
    lookup_field = 'id'
    serializer_class = ListProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = ProductModel.objects.all()



class ProductDetailAPIView(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = ProductModel.objects.all()
   
    
class UpdateProductAPIView(generics.UpdateAPIView):
    lookup_field = 'id'
    serializer_class = CreateProductSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = ProductModel.objects.all()
    
class DeleteProductAPIView(generics.DestroyAPIView):
    lookup_field = 'id'
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = ProductModel.objects.all()
    

class CreateCatogoeryAPIView(generics.CreateAPIView):
    lookup_field = 'id'
    serializer_class = CreateCategorySerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = CategoryModel.objects.all()


class UpdateCategoryAPIView(generics.UpdateAPIView):
    lookup_field = 'id'
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = CategoryModel.objects.all()
    

class CategoryListAPIView(generics.ListAPIView):
    lookup_field = 'id'
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = CategoryModel.objects.all()

class CategoryDetailAPIView(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = CategoryModel.objects.all()

class DeleteCategoryAPIView(generics.DestroyAPIView):
    lookup_field = 'id'
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = CategoryModel.objects.all()


class CreateManufacturerAPIView(generics.CreateAPIView):
    lookup_field = 'id'
    serializer_class = CreateManufacturerSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = ManufacturerModel.objects.all()


class UpdateManufacturerAPIView(generics.UpdateAPIView):
    lookup_field = 'id'
    serializer_class = CreateManufacturerSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = ManufacturerModel.objects.all()
    


class ManufacturerListAPIView(generics.ListAPIView):
    lookup_field = 'id'
    serializer_class = ListManufactuererSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = ManufacturerModel.objects.all()


class OtherProductsAPIView(APIView):

    def get(self, request, id=None):
        lookup_field = 'id'
        products = ProductModel.objects.filter(manufacturer_id=id)
        serializer =  ListProductSerializer(products, many=True)
        # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return Response({'data':serializer.data, 'status': status.HTTP_200_OK, 'msg': 'products fetched successful'})


class DeleteManufacturerAPIView(generics.DestroyAPIView):
    lookup_field = 'id'
    serializer_class = ListManufactuererSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = ManufacturerModel.objects.all()

class ManufacturerDetailAPIView(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = CreateManufacturerSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ManufacturerModel.objects.all()


class ProductsByCategoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, id=None):
        lookup_field = 'id'
        products = ProductModel.objects.filter(category_id=id)
        serializer =  ListProductSerializer(products, many=True)
        # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return Response({'data':serializer.data, 'status': status.HTTP_200_OK, 'msg': 'products fetched successful'})



class SearchAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    # serializer_class = [SearchSerializer]
    def get(self, request, *args, **kwargs):
        try:
            query = request.query_params.get('q', '').strip()
            if not query:
                return Response(
                    {"results": []},
                    status=status.HTTP_200_OK
                )

            # Search products and categories
            product_results = ProductModel.objects.filter(
                Q(name__icontains=query)
            )[:5]  # Limit to 5 results
            category_results = CategoryModel.objects.filter(
                Q(name__icontains=query)
            )[:5]

            # Combine results
            suggestions = [
                {"id": product.id, "name": product.name, "type": "product"}
                for product in product_results
            ] + [
                {"id": category.id, "name": category.name, "type": "category"}
                for category in category_results
            ]

            serializer = SearchSerializer(suggestions, many=True)
            return Response(
                 serializer.data,
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(f"Error in search suggestions: {str(e)}")
            return Response(
                {"message": "An error occurred while fetching suggestions."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )