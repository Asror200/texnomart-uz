from django.db.models import Avg
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, \
    RetrieveDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from product.models import Product
from product.permissions import IsAdminOrReadOnly
from product.serializers import ProductSerializer, ProductDetailSerializer
from django.core.cache import cache
from product.filter import ProductFilter


class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filterset_class = ProductFilter

    def get_queryset(self):
        cache_key = 'product_list'
        queryset = cache.get(cache_key)
        if queryset is None:
            queryset = (Product.objects.prefetch_related('comments', 'users_like', 'images')
                        .annotate(avg_rating=Avg('comments__rating')).all())

            cache.set(cache_key, queryset, timeout=60)
        return queryset


class ProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        cache_key = f'products_detail_{self.request.user.id}'
        print(cache_key)
        cached = cache.get(cache_key)
        if cached is None:
            queryset = Product.objects.select_related('category').prefetch_related('comments', 'users_like',
                                                                                   'images', 'attributes',
                                                                                   'attributes__attribute',
                                                                                   'attributes__value').all()
            cache.set(cache_key, queryset, timeout=60)
            return queryset
        return cached


class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class ProductUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDeleteAPIView(RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
