import uuid
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from config import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django_mysql.models.functions import JSONField
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from django.utils import timezone
from ckeditor.fields import RichTextField
from uuid import uuid4

# Create your models here.


class Customer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=255)
    customer_address = models.CharField(max_length=700, blank=True)

    class Meta:
        permissions = [
            ('send_private_email', 'Can send private email to customers'),
        ]

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @classmethod
    def save_or_update(cls, user, **kwargs):
        # اگر آدرس برای مشتری موجود باشد، آن را به‌روزرسانی می‌کند. در غیر این صورت یک آدرس جدید ایجاد می‌کند.
        customer, created = cls.objects.update_or_create(user=user, defaults=kwargs)
        return customer

class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='user_address')
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=500)


    def full_address(self):
        return f'{self.province} , {self.city} , {self.street}...'

    @classmethod
    def save_or_update(cls, customer, **kwargs):
        # اگر آدرس برای مشتری موجود باشد، آن را به‌روزرسانی می‌کند. در غیر این صورت یک آدرس جدید ایجاد می‌کند.
        address, created = cls.objects.update_or_create(customer=customer, defaults=kwargs)
        return address

class Category(MPTTModel):
    fa_name = models.CharField(max_length=100, unique=True, verbose_name=_('category fa-name'))
    en_name = models.CharField(max_length=100, unique=True, verbose_name=_('category en-name'))
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['fa_name']

    class Meta:
        unique_together = ['fa_name', 'parent']

    def __str__(self):
        return self.fa_name

    def get_absolute_url(self):
        return reverse('category_detail', args=[self.pk])


class Brand(models.Model):
    fa_name = models.CharField(max_length=100, unique=True, verbose_name=_('fa-name'))
    en_name = models.CharField(max_length=100, unique=True, verbose_name=_('en-name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('brand description'))
    logo = models.ImageField(upload_to='brand_logo/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fa_name

    class Meta:
        unique_together = ['fa_name', 'en_name']


class AttributeCategory(models.Model):
    fa_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fa_name


class Attribute(models.Model):
    fa_name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category, related_name='attributes')
    attribute_category = models.ForeignKey(AttributeCategory, on_delete=models.PROTECT, related_name='single_attribute')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     unique_together = ['fa_name', 'attribute_category']

    def __str__(self):
        return f'{self.fa_name} : {self.attribute_category}'

    @classmethod
    def save_or_update(cls, fa_name, attribute_category, **kwargs):
        # اگر آدرس برای مشتری موجود باشد، آن را به‌روزرسانی می‌کند. در غیر این صورت یک آدرس جدید ایجاد می‌کند.
        attribute, created = cls.objects.update_or_create(fa_name=fa_name, attribute_category=attribute_category, defaults=kwargs)
        return attribute


class Color(models.Model):
    fa_name = models.CharField(max_length=100, unique=True, blank=True, verbose_name=_('fa-name'))
    en_name = models.CharField(max_length=100, unique=True, blank=True, verbose_name=_('en-name'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.en_name

    def serialize_color(self):
        return self.fa_name


class Size(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name=_('size'))

    def __str__(self):
        return self.title

    def serialize_size(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_('tags'))

    def __str__(self):
        return self.name


class Product(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ]
    RATE_CHOICES = [('v', 'Very Bad'), ('b', 'Bad'), ('n', 'Normal'), ('g', 'Good'), ('p', 'Perfect')]
    fa_name = models.CharField(max_length=255, verbose_name=_('Farsi Product Name'))
    en_name = models.CharField(max_length=255, verbose_name=_('English Product Name'))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name=_('Category'))
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products', verbose_name=_('Brand'))
    model = models.CharField(max_length=255, blank=True, verbose_name=_('Product Model'))
    sizes = models.ManyToManyField(Size, blank=True, related_name='products', verbose_name=_('Product Sizes'))
    slug = models.SlugField(max_length=255, blank=True, null=True)
    short_description = models.CharField(max_length=5000, verbose_name=_('Product Short Description'))
    full_description = RichTextField(verbose_name=_('Product Full Description'))
    thumbnail = models.ImageField(upload_to='covers/product_thumbnail/')
    images = models.ManyToManyField('Image', blank=True, related_name='products', verbose_name=_('Product Images'))
    attributes = models.ManyToManyField(
        Attribute,
        through='AttributeValue',  # مدل میانی برای ذخیره اطلاعات اضافی
        related_name='products',  # نام مربوط به ارتباط از سوی مدل Attribute
        verbose_name=_('Product Attribute')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name=_('Product Gender'))
    is_active = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, verbose_name=_('Product Tags'))
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveBigIntegerField(default=0)

    class Meta:
        unique_together = ['fa_name', 'brand', 'model']

    def __str__(self):
        return self.fa_name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.pk])

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.category.en_name}{self.brand.en_name}{self.en_name}')
        super(Product, self).save(*args, **kwargs)

    def serialize(self):

        return {
            'id': self.id,
            'fa_name': self.fa_name,
            'en_name': self.en_name,
            'category': self.category.fa_name,
            'brand': self.brand.fa_name if self.brand else '',
            'model': self.model,
            'sizes': [size.serialize_size() for size in self.sizes.all()],
            'slug': self.slug,
            'short_description': self.short_description,
            'full_description': self.full_description,
            'thumbnail': self.thumbnail.url,
            'images': [image.image for image in self.images.all()],
            'attribute': [attribute.fa_name for attribute in self.attribute.all()],
            'gender': self.get_gender_display(),
            'is_active': self.is_active,
            'tags': [tag.name for tag in self.tags.all()],
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'views': self.views,
            # ... دیگر فیلدهای خودتان
        }


class Discount(models.Model):
    amount = models.FloatField(unique=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.amount)

    def serialize_amount(self):
        return self.amount

class AttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='attribute_values')
    attribute = models.ForeignKey(Attribute, on_delete=models.PROTECT, related_name='value')
    value = models.TextField(verbose_name=_('Values of Attribute'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.value[:10]

    @classmethod
    def save_or_update(cls, product, attribute, **kwargs):
        # اگر آدرس برای مشتری موجود باشد، آن را به‌روزرسانی می‌کند. در غیر این صورت یک آدرس جدید ایجاد می‌کند.
        attribute_value, created = cls.objects.update_or_create(product=product, attribute=attribute, defaults=kwargs)
        return attribute_value

    # def clean(self):
    #     # بررسی وجود مقادیر تکراری برای "product" و "attribute"
    #     if AttributeValue.objects.filter(product=self.product, attribute=self.attribute).exclude(pk=self.pk).exists():
    #         raise ValidationError("This attribute value already exists for this product.")


class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='variants', verbose_name=_('Product Variant'))
    color = models.ForeignKey(Color, on_delete=models.PROTECT, related_name='color_variant', verbose_name=_('Color Variant'))
    size = models.ForeignKey(Size, on_delete=models.PROTECT, default='41', related_name='variant_size', verbose_name=_('Size Variant'))
    sku = models.CharField(max_length=80, unique=True, blank=True)
    inventory = models.PositiveIntegerField(default=0, verbose_name=_('Variant Inventory'))
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['product', 'size', 'color']

    def clean(self):
        # بررسی کنید که آیا اندازه واریانت واقعاً برای همان محصولی است که در آن تعریف شده است یا خیر
        if self.size not in self.product.sizes.all():
            raise serializers.ValidationError('The size of this variant does not belong to the product.')

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = slugify(f'{self.created_at}{self.product.category.en_name}{self.product.en_name}{self.color.en_name}{str(self.size.title)}')
        if self.inventory == 0 or self.inventory is None:
            raise serializers.ValidationError('the minimum of inventory each variant is one(1).please try again.')
        super(Variant, self).save()

    def __str__(self):
        return f'ID:{self.id}, Name:{self.product} ,Color:{self.color} ,Quantity:{self.inventory} ,Size:{self.size}'


class VariantPricing(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, unique=True, related_name='variant_price')
    price = models.PositiveIntegerField()
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT, blank=True, null=True, related_name='price')

    class Meta:
        unique_together = ['variant', 'price']

    def __str__(self):
        return str(self.price)

    def serialize_price(self):
        return self.price


class Image(models.Model):
    image = models.ImageField(upload_to='covers/product_image/', verbose_name=_('Product Image'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(f'id: {self.id}')


class ProductComment(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_CANCEL = 'na'
    COMMENT_STATUS_CHOICES = [(COMMENT_STATUS_WAITING, 'waiting'), (COMMENT_STATUS_APPROVED, 'approved'),
                              (COMMENT_STATUS_CANCEL, 'Not approved')]

    PRODUCT_STARS = (('1', 'Very Bad'), ('2', 'Bad'), ('3', 'normal'), ('4', 'Good'), ('5', 'Perfect'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Author Comment'))
    body = models.TextField(verbose_name=_('Comment Text'))
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    product_stars = models.CharField(max_length=1, choices=PRODUCT_STARS, verbose_name=_('Rate of Product'))
    comment_status = models.CharField(max_length=2, choices=COMMENT_STATUS_CHOICES, default=COMMENT_STATUS_APPROVED)

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.product.pk])


class Order(models.Model):
    ORDER_STATUS_PAID = 'p'
    ORDER_STATUS_UNPAID = 'u'
    ORDER_STATUS_CANCELED = 'c'

    STATUS_CHOICES = (
        (ORDER_STATUS_PAID, 'paid'),
        (ORDER_STATUS_UNPAID, 'unpaid'),
        (ORDER_STATUS_CANCELED, 'cancel')
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='order')
    address = models.CharField(_('address'), max_length=700)
    order_note = models.CharField(_('Order Note'), max_length=1000, blank=True)
    post_code = models.CharField(_('Post Code'), max_length=25)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=ORDER_STATUS_UNPAID)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    def __str__(self):
        return f'order id : {self.id} , customer : {self.customer.user.first_name}'

    def get_total_price(self):
        return sum(item.quantity * item.price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.PositiveIntegerField()
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT, blank=True, null=True, related_name='order_items')

    @classmethod
    def save_or_update(cls, order, variant, **kwargs):
        # اگر آدرس برای مشتری موجود باشد، آن را به‌روزرسانی می‌کند. در غیر این صورت یک آدرس جدید ایجاد می‌کند.
        order_item, created = cls.objects.update_or_create(order=order, variant=variant, defaults=kwargs)
        return order_item

    def __str__(self):
        return f'order id : {self.order.id} , product : {self.variant.product.fa_name}, quantity : {self.quantity}, price : {self.price}'

    def save(self, *args, **kwargs):
        # Calculate price and discount from VariantPricing
        variant_pricing = self.variant.variant_price.first()  # Get the first VariantPricing object related to the variant
        if variant_pricing is None:
            raise serializers.ValidationError('No pricing found for this variant.')

        self.price = variant_pricing.price   # Set price to the price of VariantPricing or 0 if it doesn't exist
        self.discount = variant_pricing.discount  # Set discount to the discount of VariantPricing or None if it doesn't exist
        super().save(*args, **kwargs)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.PositiveIntegerField()
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT, blank=True, null=True, related_name='cart_items')

    @classmethod
    def save_or_update(cls, cart, variant, **kwargs):
        # اگر آدرس برای مشتری موجود باشد، آن را به‌روزرسانی می‌کند. در غیر این صورت یک آدرس جدید ایجاد می‌کند.
        cart_item, created = cls.objects.update_or_create(cart=cart, variant=variant, defaults=kwargs)
        return cart_item

    def __str__(self):
        return f'order id : {self.cart.id} , product : {self.variant.product.fa_name}, quantity : {self.quantity}, price : {self.price}'

    def save(self, *args, **kwargs):
        # Calculate price and discount from VariantPricing
        variant_pricing = self.variant.variant_price.first()  # Get the first VariantPricing object related to the variant
        if variant_pricing is None:
            raise serializers.ValidationError('No pricing found for this variant.')

        self.price = variant_pricing.price   # Set price to the price of VariantPricing or 0 if it doesn't exist
        self.discount = variant_pricing.discount  # Set discount to the discount of VariantPricing or None if it doesn't exist
        super().save(*args, **kwargs)



