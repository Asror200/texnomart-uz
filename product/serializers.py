from inspect import Attribute

from django.db.models import Avg
from rest_framework import serializers

from product.models import Category, Product, AttributeKey, AttributeValue, ProductAttribute, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'image']
        read_only_fields = ['id', 'slug']

    def get_image(self, obj):
        if obj.image:
            image_url = obj.image.url
            request = self.context.get('request')
            return request.build_absolute_uri(image_url)


class ProductSerializer(serializers.ModelSerializer):
    user_like = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()
    avg_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity', 'discount',
                  'user_like', 'discounted_price', 'avg_rating', 'primary_image', 'category', 'description']
        read_only_fields = ['primary_image', 'discounted_price', 'users_like']
        write_only_fields = ['category']

    def get_user_like(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.users_like.all()
        return False

    def get_primary_image(self, obj):
        primary_image = next((image for image in obj.images.all() if image.is_primary), None)
        return primary_image.image.url if primary_image else None


class CategoryDetailSerializer(CategorySerializer):
    products = ProductSerializer(many=True, read_only=True)
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'image', 'products_count', 'products']

    def get_products_count(self, obj):
        return obj.products.count()


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']
        read_only_fields = ['id']


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['attribute', 'value']

    def to_representation(self, instance):
        return {instance.attribute.key: instance.value.value}


class ProductDetailSerializer(ProductSerializer):
    images = ImageSerializer(many=True, read_only=True)
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    user_like = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity', 'discount', 'user_like', 'comment_count', 'images', 'attributes']

    def get_attributes(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.attributes.all()

    def get_images(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.images.all()

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_user_like(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.users_like.all()
        return False


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['id', 'value']
        read_only_fields = ['id']


class AttributeKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeKey
        fields = ['id', 'key']
        read_only_fields = ['id']
