from django.db import models
from users.models import User
from uuslug import slugify


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category')
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    discount = models.FloatField(null=True, blank=True)
    slug = models.SlugField(blank=True)
    users_like = models.ManyToManyField(User, related_name='products', blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    @property
    def discounted_price(self):
        if self.discount and self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return 0

    def __str__(self):
        return self.name


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name


class AttributeKey(models.Model):
    key = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.key


class AttributeValue(models.Model):
    value = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.value


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, related_name='attributes', on_delete=models.CASCADE)
    attribute = models.ForeignKey(AttributeKey, related_name='attributes', on_delete=models.CASCADE)
    value = models.ForeignKey(AttributeValue, related_name='attribute_values', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        ZERO = 0
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.ZERO.value)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    text = models.TextField()
    image = models.FileField(upload_to='comments', null=True, blank=True)
    is_clear = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.product} - {self.user}'
