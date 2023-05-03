from django.urls import path
from .apiViews import (
        UpdateCategoryAPIView, UpdateProductAPIView, 
        ProductDetailAPIView, CreateCatogoeryAPIView, 
        CategoryListAPIView, ListProductAPIView, 
        DeleteCategoryAPIView, CreateProductAPIView,
        DeleteProductAPIView
    )

app_name = 'products'
urlpatterns = [
    path('add-product', CreateProductAPIView.as_view(), name='create-product'),
    path('update-product/<uuid:id>', UpdateProductAPIView.as_view(), name='update-product'),
    path('list', ListProductAPIView.as_view(), name='product-lis'),
    path('product-detail/<uuid:id>',ProductDetailAPIView.as_view(), name='product-detail' ),
    path('delete-product/<uuid:id>', DeleteProductAPIView.as_view(), name='delete-product'),
    path('add-category', CreateCatogoeryAPIView.as_view(), name='create-category'),
    path('update-category/<uuid:id>', UpdateCategoryAPIView.as_view(), name='update-category'),
    path('list-category', CategoryListAPIView.as_view(), name='category-list'),
    path('delete-category/<uuid:id>', DeleteCategoryAPIView.as_view(), name='category-delete')
] 