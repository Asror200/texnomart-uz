import json
import os
from datetime import datetime

from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

from config.settings import EMAIL_DEFAULT_SENDER, BASE_DIR
from product.models import Product, Category
from users.models import User
from product.views import category, products


@receiver(post_save, sender=Category)
def create_user_profile(sender, created, instance, **kwargs):
    if created:
        print("Signal received, sending email...")
        subject = 'A new category was created'
        message = f'{instance.title} was created'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all() if user.email]
        send_mail(subject, message, from_email, recipient_list)


@receiver(pre_delete, sender=Category)
def pre_delete_customer(sender, instance, **kwargs):
    user_data = {
        'id': instance.id,
        'title': instance.title,
        'slug': instance.slug,

    }

    date = datetime.now().strftime("%Y,%b")

    file_path = os.path.join(BASE_DIR, 'product/deleted_data/deleted_category', f'{date}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(user_data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


@receiver(post_save, sender=Product)
def create_user_profile(sender, instance, **kwargs):
    if kwargs['created']:
        subject = 'A new product was added'
        message = f'{instance.name} was added.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all() if user.email]
        send_mail(subject, message, from_email, recipient_list)


@receiver(pre_delete, sender=Product)
def pre_delete_customer(sender, instance, **kwargs):
    user_data = {
        'id': instance.id,
        'name': instance.name,
        'description': instance.description,
        'price': str(instance.price),
        'quantity': str(instance.quantity),
        'discount': str(instance.discount),
        'slug': instance.slug,
        'category': str(instance.category),
    }

    date = datetime.now().strftime("%Y,%b")

    file_path = os.path.join(BASE_DIR, 'product/deleted_data/deleted_product', f'{date}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(user_data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


""" CACHE """


@receiver(post_save, sender=Category)
def clear_category_cache_on_save(sender, instance, **kwargs):
    cache.delete(category.CategoryDetail, 'category_list')


@receiver(post_delete, sender=Category)
def clear_category_cache_on_delete(sender, instance, **kwargs):
    cache.delete(category.CategoryDetail, 'category_list')


""" PRODUCTS"""


@receiver(post_save, sender=Product)
def clear_product_cache_on_save(sender, instance, **kwargs):
    cache.delete(products.ProductDetailAPIView, 'product_list')


@receiver(post_delete, sender=Product)
def clear_product_cache_on_delete(sender, instance, **kwargs):
    cache.delete(products.ProductDetailAPIView, 'product_list')
