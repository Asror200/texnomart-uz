from django.urls import path
from product.views import category, products, attribute

urlpatterns = [

    # SHOW list of CATEGORIES
    path('categories/', category.CategoryList.as_view(), name='category-list'),
    path('category/<slug:slug>/', category.CategoryDetail.as_view(), name='category-detail'),

    # CRUD over CATEGORIES
    path('add-category/', category.CategoryCreateAPIView.as_view(), name='add-category'),
    path('category/edit/<slug:slug>/', category.CategoryUpdateAPIView.as_view(), name='category-edit'),
    path('category/delete/<slug:slug>/', category.CategoryDeleteAPIView.as_view(), name='category-delete'),

    # SHOW list of PRODUCTS
    path('products/', products.ProductListAPIView.as_view(), name='product-list'),
    path('product/detail/<int:pk>/', products.ProductDetailAPIView.as_view(), name='product-detail'),

    # CRUD over PRODUCTS
    path('add-product/', products.ProductCreateAPIView.as_view(), name='add-product'),
    path('product/edit/<int:pk>/', products.ProductUpdateAPIView.as_view(), name='product-update'),
    path('product/delete/<int:pk>/', products.ProductDeleteAPIView.as_view(), name='product-delete'),

    # SHOW list of ATTRIBUTE KEY and VALUE
    path('attribute-values/', attribute.AttributeValueListAPIView.as_view(), name='attribute-values-list'),
    path('attribute-keys/', attribute.AttributeKeyListAPIView.as_view(), name='attribute-keys-list'),

]
