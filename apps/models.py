from django.contrib.auth.models import User
from django.db.models import Model, CharField, PositiveIntegerField, TextField, JSONField, ForeignKey, CASCADE, \
    PositiveSmallIntegerField, ImageField, DateTimeField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    name = CharField(max_length=255)
    parent = TreeForeignKey('self', CASCADE, related_name='children', null=True, blank=True)

    class MPTTMeta:
        # order_insertion_by = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Brand(Model):
    name = CharField(max_length=255, null=True, blank=True)


class Product(Model):
    title = CharField(max_length=255)
    description = TextField(null=True, blank=True)
    price = PositiveIntegerField(default=0)
    specification = JSONField(null=True, blank=True)
    brand = ForeignKey(Brand, CASCADE, related_name='products')
    category = ForeignKey(Category, CASCADE, related_name='products')
    discount = PositiveSmallIntegerField(default=0)
    view_count = PositiveIntegerField(default=0)
    quantity = PositiveIntegerField(default=0)
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    @property
    def discount_price(self):
        return self.price - self.price * self.discount / 100


class ProductImage(Model):
    image = ImageField(upload_to='products/')
    product = ForeignKey(Product, CASCADE, related_name='images')


class Favourite(Model):
    product = ForeignKey(Product, CASCADE, related_name='favourites')
    user = ForeignKey(User, CASCADE, related_name='favourites')


class Cart(Model):
    product = ForeignKey(Product, on_delete=CASCADE, related_name='carts')
    booker = ForeignKey(User, on_delete=CASCADE, related_name='carts')
    product_count = PositiveIntegerField(default=1)