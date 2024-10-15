from django.core.cache import cache
from rest_framework import filters
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Category
from product.permissions import IsAdminOrReadOnly
from product.serializers import CategorySerializer, CategoryDetailSerializer


class CategoryList(APIView):
    permission_classes = [AllowAny]
    search_fields = ['title']
    filter_backends = (filters.SearchFilter,)

    def get(self, request, format=None):
        search_query = request.GET.get('search', None)

        if search_query:
            cache_key = f'category_list_search_{search_query}'
            cached = cache.get(cache_key)

            if cached is None:
                categories = Category.objects.filter(title__icontains=search_query)
                serializer = CategorySerializer(categories, context={'request': request}, many=True)
                cache.set(cache_key, serializer.data, timeout=60)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(cached, status=status.HTTP_200_OK)

        cache_key = 'category_list'
        cached = cache.get(cache_key)
        if cached is None:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, context={'request': request}, many=True)
            cache.set(cache_key, serializer.data, timeout=60)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(cached, status=status.HTTP_200_OK)


class CategoryDetail(generics.RetrieveAPIView):
    serializer_class = CategoryDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        cache_key = f'category_detail_{self.request.user.id}'
        cached = cache.get(cache_key)
        if not cached:
            queryset = Category.objects.prefetch_related('products', 'products__users_like', 'products__images').all()
            cache.set(cache_key, queryset, timeout=60)
            return queryset
        return cached


class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryDeleteAPIView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'

    def delete(self, request, *args, **kwargs):
        object = self.get_object()
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
