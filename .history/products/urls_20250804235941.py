from django.urls import path
from .apiViews import (
        UpdateCategoryAPIView, UpdateProductAPIView, 
        ProductDetailAPIView, CreateCatogoeryAPIView, 
        CategoryListAPIView, ListProductAPIView, 
        DeleteCategoryAPIView, CreateProductAPIView,
        DeleteProductAPIView, ManufacturerListAPIView,
        CreateManufacturerAPIView, UpdateManufacturerAPIView, OtherProductsAPIView,
        DeleteManufacturerAPIView, CategoryDetailAPIView, ManufacturerDetailAPIView,
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
    path('category-detail/<uuid:id>', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('product-category-list/<uuid:id>', CategoryDetailAPIView.as_view(), name='category-detail'),

    path('list-category', CategoryListAPIView.as_view(), name='category-list'),
    path('delete-category/<uuid:id>', DeleteCategoryAPIView.as_view(), name='category-delete'),
    path('add-manufacturer', CreateManufacturerAPIView.as_view(), name='create-manufacturer'),
    path('update-manufacturer/<uuid:id>', UpdateManufacturerAPIView.as_view(), name='update-manufacturer'),
    path('list-manufacturer', ManufacturerListAPIView.as_view(), name='manufacturer-list'),
    path('manufacturer-detail/<uuid:id>', OtherProductsAPIView.as_view(), name='category-detail'),
    path('delete-manufacturer/<uuid:id>', DeleteManufacturerAPIView.as_view(), name='delete-manufacturer'),
]   