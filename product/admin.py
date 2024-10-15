from django.contrib import admin
from django.utils.html import format_html

from product.models import Product, Category, ProductImage, AttributeKey, AttributeValue, ProductAttribute, Comment


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'get_image')
    list_filter = ('title',)
    search_fields = ('title',)

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="rounded-circle" style="width: 50px; height: 50px;" />',
                               obj.image.url)
        return format_html('<span> No image </span>')

    get_image.short_description = 'Image'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'price', 'quantity', 'discount', 'description')
    search_fields = ('name', 'category', 'slug')
    list_filter = ('category', 'price')


@admin.register(ProductImage)
class ProductImage(admin.ModelAdmin):
    list_display = ('product', 'image')
    search_fields = ('product',)
    list_filter = ('product',)

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="rounded-circle" style="width: 50px; height: 50px;" />',
                               obj.image.url)
        return format_html('<span> No image </span>')

    get_image.short_description = 'Image'


@admin.register(AttributeKey)
class AttributeKeyAdmin(admin.ModelAdmin):
    list_display = ('key',)
    search_fields = ('key',)
    list_filter = ('key',)


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('value',)
    search_fields = ('value',)
    list_filter = ('value',)


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute', 'value')
    search_fields = ('product', 'attribute', 'value')
    list_filter = ('product', 'attribute', 'value')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'text', 'get_image')
    search_fields = ('user', 'product', 'text')
    list_filter = ('user', 'product', 'rating')

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="rounded-circle" style="width: 50px; height: 50px;" />',
                               obj.image.url)
        return format_html('<span> No image </span>')

    get_image.short_description = 'Image'
