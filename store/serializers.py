from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Count, F, Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from requests import Response
from rest_framework import serializers, status, exceptions
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from unicodedata import decimal

from config import settings
from core.models import CustomUser
from core.serializers import UserSerializer
from store import views
from store.models import Category, Brand, Customer, Address, Color, Size, AttributeCategory, Attribute, Tag, Product, \
    Discount, VariantPricing, AttributeValue, Variant, Image, ProductComment, Order, OrderItem, Cart, CartItem


class CreateCustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'province', 'city', 'street']

    def create(self, validated_data):
        if 'customer_pk' in self.context:
            customer_pk = self.context['customer_pk']
            customer = get_object_or_404(Customer, id=customer_pk)
        else:
            request = self.context.get('request')
            user = request.user
            customer = get_object_or_404(Customer, user=user)

        if Address.objects.filter(customer_id=customer.id).exists():
            address_obj = Address.objects.get(customer_id=customer.id)
            address_obj.province = validated_data['province']
            address_obj.city = validated_data['city']
            address_obj.street = validated_data['street']
            address_obj.save()
            self.instance = address_obj
            return address_obj

        address = Address.objects.create(customer_id=customer.id, **validated_data)
        address.save()
        self.instance = address
        return address

class ShowAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'customer', 'province', 'city', 'street']


class UpdateAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'province', 'city', 'street']

    def update(self, instance, validated_data):
        if 'customer_pk' in self.context:
            customer_pk = self.context['customer_pk']
            customer = get_object_or_404(Customer, id=customer_pk)
        else:
            request = self.context.get('request')
            user =request.user
            customer = get_object_or_404(Customer, user=user)

        instance.customer = customer
        instance.province = validated_data.get('province', instance.province)
        instance.city = validated_data.get('city', instance.city)
        instance.street = validated_data.get('street', instance.street)
        instance.save()
        return instance

class CreateCustomerSerializer(serializers.ModelSerializer):
    address = ShowAddressSerializer(many=True, source='user_address', read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone_number', 'customer_address', 'address']

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        user_obj = get_object_or_404(get_user_model(), id=user.id)
        user_choice = validated_data['user']
        user_choice_obj = get_object_or_404(get_user_model(), id=user_choice.id)

        if user.is_staff and user_choice.id != user.id:
            if Customer.objects.filter(user_id=user_choice.id).exists():
                message = 'already exsist the customer with this specified user-id.for change information this customer going to edit information'
                raise serializers.ValidationError(detail=message)
            else:
                customer_obj = Customer.objects.create(user_id=user_choice.id, **validated_data)
                customer_obj.save()
                self.instance = customer_obj
                return customer_obj

        elif Customer.objects.filter(user_id=user.id).exists():
            message = 'already create the customer with this user-id. for any customizing in this specified customer please go to edit information.'
            raise serializers.ValidationError(detail=message)

        else:
            customer_obj = Customer.objects.create(user_id=user.id, **validated_data)
            customer_obj.save()
            self.instance = customer_obj
            return customer_obj



class ShowCustomerSerializer(serializers.ModelSerializer):
    address = ShowAddressSerializer(many=True, source='user_address', read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone_number', 'customer_address', 'address']

class UpdateCustomerSerializer(serializers.ModelSerializer):
    address = ShowAddressSerializer(many=True, source='user_address', read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'phone_number', 'customer_address', 'address']



class CategorySerializer(serializers.ModelSerializer):
    count_product_in_every_category = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'parent', 'fa_name', 'en_name', 'image', 'is_active', 'created_at', 'updated_at',
                  'count_product_in_every_category']


class BrandSerializer(serializers.ModelSerializer):
    count_product_in_every_brand = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = Brand
        fields = ['id', 'fa_name', 'en_name', 'description', 'logo', 'created_at', 'updated_at',
                  'count_product_in_every_brand']


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['amount', 'description']

class CreateVariantPricingSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    price_after_tax = serializers.SerializerMethodField()


    class Meta:
        model = VariantPricing
        fields = ['id', 'variant', 'price', 'discount', 'product_name', 'price_after_tax']

    def get_product_name(self, instance):
        return instance.variant.product.fa_name  # یا هر فیلد دلخواه دیگری از مدل Product


    def get_price_after_tax(self, variant_pricing):
        return round(variant_pricing.price * Decimal(1.09), 2)

    def create(self, validated_data):
        if 'variant_pk' in self.context:
            variant_pk = self.context['variant_pk']
            variant = get_object_or_404(Variant, id=variant_pk)
        else:
            variant_pk = validated_data['variant'].id
            variant = get_object_or_404(Variant, id=variant_pk)

        if validated_data['discount']:
            discount = get_object_or_404(Discount, id=validated_data['discount'].id)

        if VariantPricing.objects.filter(variant_id=variant_pk).exists():
            message = 'The pricing value already make it for this product variant '
            raise serializers.ValidationError(detail=message)

        variant_pricing_obj = VariantPricing.objects.create(variant_id=variant_pk, **validated_data)
        variant_pricing_obj.save()
        self.instance = variant_pricing_obj
        return variant_pricing_obj


class UpdateVariantPricingSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    price_after_tax = serializers.SerializerMethodField()

    class Meta:
        model = VariantPricing
        fields = ['id', 'variant', 'product_name', 'price', 'discount',  'price_after_tax']

    def get_product_name(self, instance):
        return instance.variant.product.fa_name  # یا هر فیلد دلخواه دیگری از مدل Product


    def get_price_after_tax(self, variant_pricing):
        return round(variant_pricing.price * Decimal(1.09), 2)


    def update(self, instance, validated_data):
        if 'variant_pk' in self.context:
            variant_pk = self.context['variant_pk']
            variant = get_object_or_404(Variant, id=variant_pk)

        else:
            variant = validated_data['variant']
            variant = get_object_or_404(Variant, id=variant.id)

        if instance.variant != variant:
            message = 'you can not change the product'
            raise serializers.ValidationError(detail=message)

        if validated_data['discount']:
            discount = get_object_or_404(Discount, id=validated_data['discount'].id)

        instance.price = validated_data.get('price', instance.price)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.save()
        return instance


class VPDetailForVariantSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    price_after_tax = serializers.SerializerMethodField()

    class Meta:
        model = VariantPricing
        fields = ['id', 'product_name', 'price', 'discount', 'price_after_tax',]

    def get_product_name(self, instance):
        return instance.variant.product.fa_name  # یا هر فیلد دلخواه دیگری از مدل Product

    def get_price_after_tax(self, variant_pricing):
        return round(variant_pricing.price * Decimal(1.09), 2)


class CreateVariantSerializer(serializers.ModelSerializer):
    variant_price = VPDetailForVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Variant
        fields = ['id', 'product', 'color', 'size', 'inventory', 'is_active', 'variant_price', 'sku']

    def validate_size(self, value):
        """
        بررسی می‌کند که سایز موجود در محصول باشد
        """
        if 'product_pk' in self.context:
            product_id = self.context['product_pk']
            product = get_object_or_404(Product, id=product_id)
            if value not in product.sizes.all():
                raise serializers.ValidationError('The size does not belong to the product.')
            return value

        product_id = self.initial_data.get('product')
        product = get_object_or_404(Product, id=product_id)
        if value not in product.sizes.all():
            raise serializers.ValidationError('The size does not belong to the product.')
        return value

    def create(self, validated_data):
        if 'product_pk' in self.context:
            product_pk = self.context['product_pk']
            product = get_object_or_404(Product, id=product_pk)
        else:
            product_pk = validated_data['product'].id
            product = get_object_or_404(Product, id=product_pk)

        size = validated_data['size']
        color = validated_data['color']

        if Variant.objects.filter(product_id=product_pk, color_id=color.id, size_id=size.id).exists():
            message = 'Variant with this color and size already exists for specified product '
            raise serializers.ValidationError(detail=message)

        variant = Variant.objects.create(product_id=product_pk, **validated_data)
        variant.save()
        self.instance = variant
        return variant

class ShowVariantSerializer(serializers.ModelSerializer):
    variant_price = VPDetailForVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Variant
        fields = ['id', 'product', 'color', 'size', 'inventory', 'is_active', 'variant_price', 'sku']

class UpdateVariantSerializer(serializers.ModelSerializer):
    variant_price = VPDetailForVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Variant
        fields = ['id', 'product', 'color', 'size', 'inventory', 'is_active', 'variant_price', 'sku']

    def update(self, instance, validated_data):
        if 'product_pk' in self.context:
            product_id = self.context['product_pk']
            product = get_object_or_404(Product, id=product_id)
        else:
            product_id = validated_data['product'].id
            product = get_object_or_404(Product, id=product_id)

        size_id = validated_data['size'].id
        size = get_object_or_404(Size, id=size_id)
        color_id = validated_data['color'].id
        color = get_object_or_404(Color, id=color_id)


        # این تیکه از کد هیچ.چوفت اجرا نمیشود
        # چون این سریالازر از طریق مدل به قیلد
        # یونیک تبدیل شده و قابلیت آپدیت یگانه
        # سه مقداری که به یونیک دادیم رو نداره

        if Variant.objects.filter(product_id=product_id, size_id=size_id, color_id=color_id).exists():
            if instance.product != validated_data['product']:
                message = 'in this path: you can not change the product'
                raise serializers.ValidationError(detail=message)
            instance.product = product
            instance.size = size
            instance.color = color
            instance.sku = None
            instance.inventory = validated_data.get('inventory', instance.inventory)
            instance.is_active = validated_data['is_active']
            instance.clean()
            instance.save()
            return instance


        if instance.product != validated_data['product']:
            message = 'in this path: you can not change the product'
            raise serializers.ValidationError(detail=message)
        instance.product = product
        instance.size = size
        instance.color = validated_data['color']
        instance.sku = None
        instance.inventory = validated_data.get('inventory', instance.inventory)
        instance.is_active = validated_data['is_active']
        instance.clean()
        instance.save()
        return instance


class CreateAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['id', 'product', 'attribute', 'value']

    def create(self, validated_data):
        if 'attribute_pk' in self.context:
            attribute_pk = self.context['attribute_pk']
        else:
            attribute_pk = validated_data.get('attribute').id

        product_pk = validated_data['product'].id
        attribute = get_object_or_404(Attribute, id=attribute_pk)

        if AttributeValue.objects.filter(attribute_id=attribute_pk, product_id=product_pk).exists():
            message = "Attribute Value with this Attribute already exists for the specified product."
            raise serializers.ValidationError(detail=message)

        attribute_value = AttributeValue.objects.create(attribute_id=attribute_pk, **validated_data)
        attribute_value.save()
        self.instance = attribute_value
        return attribute_value

class ShowAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['id', 'product', 'attribute', 'value']


class UpdateAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['id', 'product', 'attribute', 'value', ]

    def update(self, instance, validated_data):
        if 'attribute_pk' in self.context:
            attribute_pk = self.context['attribute_pk']
            attribute = get_object_or_404(Attribute, id=attribute_pk)
        else:
            attribute_pk = validated_data['attribute'].id
            attribute = get_object_or_404(Attribute, id=attribute_pk)

        product_pk = validated_data['product'].id
        product = get_object_or_404(Product, id=product_pk)




        if AttributeValue.objects.filter(product_id=validated_data['product'].id, attribute_id=attribute_pk, value=validated_data['value']).exists():
            message = "Attribute Value with this Value and Attribute already exists for the specified product."
            raise serializers.ValidationError(detail=message)

        if AttributeValue.objects.filter(product=validated_data['product'], attribute_id=attribute_pk).exists():
            message = "Attribute Value with this Attribute already exists for the specified product."
            raise serializers.ValidationError(detail=message)

        instance.attribute = attribute
        instance.value = validated_data.get('value', instance.value)
        instance.product = validated_data.get('product', instance.product)
        instance.save()
        return instance


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    count_sizes = serializers.SerializerMethodField()
    product_variants = ShowVariantSerializer(many=True, source='variant', read_only=True)
    attributes_values = ShowAttributeValueSerializer(many=True, read_only=True)
    images = serializers.PrimaryKeyRelatedField(many=True, queryset=Image.objects.all())  # یا HyperlinkedRelatedField نیز می‌توانید استفاده کنید

    class Meta:
        model = Product
        fields = ['id', 'fa_name', 'en_name', 'model', 'slug', 'short_description', 'full_description', 'gender',
                  'is_active', 'views', 'count_sizes', 'category', 'brand', 'thumbnail', 'images', 'sizes', 'attributes', 'attributes_values',
                  'tags', 'product_variants']

    def get_count_sizes(self, products):
        return products.sizes.count()

    def create(self, validated_data):
        sizes_data = validated_data.pop('sizes')
        tags_data = validated_data.pop('tags')
        images_data = validated_data.pop('images')

        if 'category_pk' in self.context:
            category_pk = self.context['category_pk']
            category = get_object_or_404(Category, id=category_pk)

            product = Product.objects.create(category_id=category_pk, **validated_data)
            product.save()

        elif 'brand_pk' in self.context:
            brand_pk = self.context['brand_pk']
            brand = get_object_or_404(Brand, id=brand_pk)

            product = Product.objects.create(brand_id=brand_pk, **validated_data)
            product.save()
        else:
            product = Product.objects.create(**validated_data)
            product.save()

        for size_id in sizes_data:
            product.sizes.add(size_id)
        for tag_id in tags_data:
            product.tags.add(tag_id)
        for image_id in images_data:
            product.images.add(image_id)

        product.save()
        self.instance = product
        return product


class ColorSerializer(serializers.ModelSerializer):
    variants = ShowVariantSerializer(many=True, source='color_variant', read_only=True)

    class Meta:
        model = Color
        fields = ['id', 'fa_name', 'en_name', 'created_at', 'updated_at', 'variants']


class SizeSerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Size
        fields = ['id', 'title', 'products']



class AttributeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeCategory
        fields = ['id', 'fa_name', 'created_at', 'updated_at']

class CreateAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'fa_name', 'categories', 'attribute_category']

    def create(self, validated_data):

        if 'attribute_category_pk' in self.context:
            attribute_category_pk = self.context['attribute_category_pk']
            attribute_category = get_object_or_404(AttributeCategory, id=attribute_category_pk)
        else:
            attribute_category_pk = validated_data['attribute_category'].id
            attribute_category = get_object_or_404(AttributeCategory, id=attribute_category_pk)

        categories_data = validated_data.pop('categories')

        if Attribute.objects.filter(Q(attribute_category_id=attribute_category_pk) & Q(fa_name=validated_data['fa_name'])).exists():
            attribute_obj = Attribute.objects.get(Q(attribute_category_id=attribute_category_pk) & Q(fa_name=validated_data['fa_name']))

            for category_id in categories_data:
                attribute_obj.categories.add(category_id)
            attribute_obj.save()
            self.instance = attribute_obj
            return attribute_obj


        attribute_obj = Attribute.objects.create(attribute_category_id=attribute_category_pk, **validated_data)
        for category_id in categories_data:
            attribute_obj.categories.add(category_id)
        attribute_obj.save()
        self.instance = attribute_obj
        return attribute_obj


class ShowAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'fa_name', 'categories', 'attribute_category']


class UpdateAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'fa_name', 'categories', 'attribute_category']


    def update(self, instance, validated_data):
        if 'attribute_category_pk' in self.context:
            attribute_category_pk = self.context['attribute_category_pk']
            attribute_category = get_object_or_404(AttributeCategory, id=attribute_category_pk)
        else:
            attribute_category_pk = validated_data['attribute_category'].id
            attribute_category = get_object_or_404(AttributeCategory, id=attribute_category_pk)

        instance.attribute_category = attribute_category
        instance.fa_name = validated_data.get('fa_name', instance.fa_name)
        categories_data = validated_data.pop('categories')

        instance.categories.clear()
        for category_id in categories_data:
            instance.categories.add(category_id)
        instance.save()
        return instance


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', ]

    # name = serializers.CharField(max_length=255)


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['amount', 'description']


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = ['id', 'body', 'product_stars']

    def validate(self, data):
        if len(data['body']) < 3:
            raise serializers.ValidationError('the body of comment must should greater than 2 character.')
        return data


    def create(self, validated_data):
        if 'request' in self.context and 'product_pk' in self.context:
            request = self.context['request']
            product_pk = self.context['product_pk']
            product = get_object_or_404(Product, id=product_pk)
            user = request.user
            validated_data['user'] = user
            product_comment_obj = ProductComment.objects.create(product_id=product_pk, **validated_data)
            product_comment_obj.save()
            return product_comment_obj
        else:
            message = 'For commenting please first login in your account'
            raise serializers.ValidationError(detail=message)


class ShowCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = ['id', 'product', 'user', 'body', 'product_stars']


class ShowOrderItemSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    price_after_discount = serializers.SerializerMethodField()
    price_after_tax = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'variant', 'quantity', 'price', 'discount', 'price_after_discount', 'price_after_tax']

    def get_price_after_tax(self, order_item):
        if order_item.discount:
            return round(((order_item.price - (order_item.price * order_item.discount.amount)) * 1.09) * order_item.quantity, 2)
        return round((order_item.price * 1.09) * order_item.quantity, 2)

    def get_price_after_discount(self, order_item):
        if order_item.discount:
            price_after_discount = (order_item.price - (order_item.price * order_item.discount.amount)) * order_item.quantity
            return price_after_discount
        return order_item.price * order_item.quantity

    def get_price(self, instance):
        return instance.price

    def get_discount(self, instance):
        if instance.discount:
            return instance.discount.amount
        return None

#
# class UpdateOrderItemSerializer(serializers.ModelSerializer):
#     price = serializers.SerializerMethodField()
#     discount = serializers.SerializerMethodField()
#     price_after_discount = serializers.SerializerMethodField()
#     price_after_tax = serializers.SerializerMethodField()
#
#     class Meta:
#         model = OrderItem
#         fields = ['id', 'order', 'variant', 'quantity', 'price', 'discount', 'price_after_discount', 'price_after_tax']
#
#     def get_price_after_tax(self, order_item):
#         if order_item.discount:
#             return round(((order_item.price - (order_item.price * order_item.discount.amount)) * 1.09) * order_item.quantity, 2)
#         return round((order_item.price * 1.09) * order_item.quantity, 2)
#
#     def get_price_after_discount(self, order_item):
#         if order_item.discount:
#             price_after_discount = (order_item.price - (order_item.price * order_item.discount.amount)) * order_item.quantity
#             return price_after_discount
#         return order_item.price * order_item.quantity
#
#     def get_price(self, instance):
#         return instance.price
#
#     def get_discount(self, instance):
#         if instance.discount:
#             return instance.discount.amount
#         return None
#
#     def update(self, instance, validated_data):
#         request = self.context['request']
#         user = request.user
#         user = get_object_or_404(get_user_model(), id=user.id)
#         customer = get_object_or_404(Customer, user_id=user.id)
#         variant_pk = validated_data['variant'].id
#         variant = get_object_or_404(Variant, id=variant_pk)
#         quantity = validated_data.get('quantity', 1)
#
#         instance.quantity = quantity
#         if instance.quantity <= 0:
#             raise serializers.ValidationError('the minimum number of quantity choices product is 1')
#         variant_pricing = instance.variant.variant_price.first()
#         instance.price = variant_pricing.price
#         instance.discount = variant_pricing.discount
#         instance.save()
#         return instance

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    address = serializers.CharField(max_length=700)
    order_note = serializers.CharField(max_length=1000)
    post_code = serializers.CharField(max_length=25)

    def validate_cart_id(self, cart_id):
        try:
            if Cart.objects.prefetch_related('items').get(id=cart_id).items.count() == 0:
                raise serializers.ValidationError('your cart is empty of product. please first select some product to add in your cart.')
        except Cart.DoesNotExist:
            raise serializers.ValidationError('dont found cart with this cart id.')
        return cart_id

    def save(self):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            request = self.context['request']
            user = request.user
            if 'customer_pk' in self.context:
                customer_pk = self.context['customer_pk']
                customer = get_object_or_404(Customer, id=customer_pk)
            else:
                customer = get_object_or_404(Customer, user_id=user.id)

            order = Order()
            order.customer = customer
            order.order_note = self.validated_data['order_note']
            order.address = self.validated_data['address']
            order.post_code = self.validated_data['post_code']
            order.save()

            cart_items = CartItem.objects.filter(cart_id=cart_id)

            order_items = list()

            for cart_item in cart_items:
                order_item = OrderItem()
                order_item.order = order
                order_item.variant_id = cart_item.variant_id
                order_item.quantity = cart_item.quantity
                order_item.price = cart_item.price
                order_item.discount_id = cart_item.discount_id

                order_items.append(order_item)

            OrderItem.objects.bulk_create(order_items)

            Cart.objects.get(id=cart_id).delete()

            return order

class AdminShowOrderSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.first_name')
    order_status = serializers.CharField(source='get_status_display', read_only=True)
    order_items = ShowOrderItemSerializer(many=True, read_only=True, source='items')
    order_total_price_after_tax = serializers.SerializerMethodField()
    order_total_price_after_discount = serializers.SerializerMethodField()
    order_total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'address', 'order_note', 'post_code',
                  'order_status', 'order_items', 'order_total_price', 'order_total_price_after_tax',
                  'order_total_price_after_discount']

    def get_order_total_price(self, order):
        return sum([item.quantity * item.variant.variant_price.first().price for item in order.items.all()])

    def get_order_total_price_after_tax(self, order):
        total_p_after_t = []
        for item in order.items.all():
            if item.discount:
                total_price_after_tax = round(
                    ((item.price - (item.price * item.discount.amount)) * 1.09) * item.quantity, 2)
                total_p_after_t.append(total_price_after_tax)
            elif item.discount is None:
                total_price_after_tax = round((item.price * 1.09) * item.quantity, 2)
                total_p_after_t.append(total_price_after_tax)
        return sum(total_p_after_t)

    def get_order_total_price_after_discount(self, order):
        total_p_after_d = []
        for item in order.items.all():
            if item.discount:
                total_price_after_discount = (item.price - (item.price * item.discount.amount)) * item.quantity
                total_p_after_d.append(total_price_after_discount)
            elif item.discount is None:
                total_price_after_discount = item.price * item.quantity
                total_p_after_d.append(total_price_after_discount)
        return sum(total_p_after_d)


class ShowOrderSerializer(serializers.ModelSerializer):
    order_status = serializers.CharField(source='get_status_display', read_only=True)
    order_items = ShowOrderItemSerializer(many=True, read_only=True, source='items')
    order_total_price_after_tax = serializers.SerializerMethodField()
    order_total_price_after_discount = serializers.SerializerMethodField()
    order_total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'address', 'order_note', 'post_code', 'order_status', 'order_items', 'order_total_price', 'order_total_price_after_tax',
                  'order_total_price_after_discount']

    def get_order_total_price(self, order):
        return sum([item.quantity * item.variant.variant_price.first().price for item in order.items.all()])

    def get_order_total_price_after_tax(self, order):
        total_p_after_t = []
        for item in order.items.all():
            if item.discount:
                total_price_after_tax = round(
                    ((item.price - (item.price * item.discount.amount)) * 1.09) * item.quantity, 2)
                total_p_after_t.append(total_price_after_tax)
            elif item.discount is None:
                total_price_after_tax = round((item.price * 1.09) * item.quantity, 2)
                total_p_after_t.append(total_price_after_tax)
        return sum(total_p_after_t)

    def get_order_total_price_after_discount(self, order):
        total_p_after_d = []
        for item in order.items.all():
            if item.discount:
                total_price_after_discount = (item.price - (item.price * item.discount.amount)) * item.quantity
                total_p_after_d.append(total_price_after_discount)
            elif item.discount is None:
                total_price_after_discount = item.price * item.quantity
                total_p_after_d.append(total_price_after_discount)
        return sum(total_p_after_d)


class UpdateOrderSerializer(serializers.ModelSerializer):
    order_status = serializers.CharField(source='get_status_display', read_only=True)
    order_items = ShowOrderItemSerializer(many=True, read_only=True, source='items')
    order_total_price_after_tax = serializers.SerializerMethodField()
    order_total_price_after_discount = serializers.SerializerMethodField()
    order_total_price = serializers.SerializerMethodField()


    class Meta:
        model = Order
        fields = ['id', 'address', 'order_note', 'post_code',
                  'order_status', 'order_items', 'order_total_price', 'order_total_price_after_tax', 'order_total_price_after_discount']

    def get_order_total_price(self, order):
        return sum([item.quantity * item.variant.variant_price.first().price for item in order.items.all()])

    def get_order_total_price_after_tax(self, order):
        total_p_after_t = []
        for item in order.items.all():
            if item.discount:
                total_price_after_tax = round(((item.price - (item.price * item.discount.amount)) * 1.09) * item.quantity, 2)
                total_p_after_t.append(total_price_after_tax)
            elif item.discount is None:
                total_price_after_tax = round((item.price * 1.09) * item.quantity, 2)
                total_p_after_t.append(total_price_after_tax)
        return sum(total_p_after_t)

    def get_order_total_price_after_discount(self, order):
        total_p_after_d = []
        for item in order.items.all():
            if item.discount:
                total_price_after_discount = (item.price - (item.price * item.discount.amount)) * item.quantity
                total_p_after_d.append(total_price_after_discount)
            elif item.discount is None:
                total_price_after_discount = item.price * item.quantity
                total_p_after_d.append(total_price_after_discount)
        return sum(total_p_after_d)


    # def update(self, instance, validated_data):
    #     if 'request' in self.context and 'customer_pk' in self.context:
    #         request = self.context['request']
    #         user = request.user
    #         user_obj = get_object_or_404(get_user_model(), id=user.id)
    #         customer_pk = self.context['customer_pk']
    #         customer = get_object_or_404(Customer, id=customer_pk)
    #
    #         instance.address = validated_data.get('address', instance.address)
    #         instance.order_note = validated_data.get('order_note', instance.order_note)
    #         instance.post_code = validated_data.get('post_code', instance.post_code)
    #         instance.save()
    #         return instance
    #
    #     else:
    #         if 'request' in self.context:
    #             request = self.context['request']
    #             user = request.user
    #             user_obj = get_object_or_404(get_user_model(), id=user.id)
    #             customer = get_object_or_404(Customer, user_id=user.id)
    #
    #             instance.address = validated_data.get('address', instance.address)
    #             instance.order_note = validated_data.get('order_note', instance.order_note)
    #             instance.post_code = validated_data.get('post_code', instance.post_code)
    #             instance.save()
    #             return instance


class CreateCartItemSerializer(serializers.ModelSerializer):
    cart_total_item = serializers.SerializerMethodField()
    price_after_discount = serializers.SerializerMethodField()
    price_after_tax = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'variant', 'quantity', 'price', 'discount', 'price_after_tax', 'price_after_discount', 'cart_total_item']

    def get_cart_total_item(self, cart_item):
        return cart_item.variant.variant_price.first().price * cart_item.quantity

    def get_price_after_tax(self, cart_item):
        if cart_item.discount:
            return round(((cart_item.price - (cart_item.price * cart_item.discount.amount)) * 1.09) * cart_item.quantity, 2)
        return round((cart_item.price * 1.09 * cart_item.quantity), 2)

    def get_price_after_discount(self, cart_item):
        if cart_item.discount:
            price_after_discount = (cart_item.price - (cart_item.price * cart_item.discount.amount)) * cart_item.quantity
            return price_after_discount
        return cart_item.price * cart_item.quantity

    def get_price(self, instance):
        return instance.price

    def get_discount(self, instance):
        if instance.discount:
            return instance.discount.amount
        return None


    def create(self, validated_data):
        if 'cart_pk' in self.context:
            cart_pk = self.context['cart_pk']
        else:
            cart_pk = validated_data['cart'].id
            # message = 'dont found any cart-id, please first create a cart and them add cart-items.'
            # raise serializers.ValidationError(detail=message)
        variant_pk = validated_data['variant'].id
        cart = get_object_or_404(Cart, id=cart_pk)
        variant = get_object_or_404(Variant, id=variant_pk)
        quantity = validated_data.get('quantity', 1)

        if CartItem.objects.filter(cart_id=cart_pk, variant_id=variant_pk).exists():
            cart_item_obj = CartItem.objects.get(cart_id=cart_pk, variant_id=variant_pk)
            cart_item_obj.variant = validated_data['variant']
            cart_item_obj.quantity += quantity
            if cart_item_obj.quantity <= 0:
                raise serializers.ValidationError('the minimum number of quantity choices product is 1')

            variant_pricing = cart_item_obj.variant.variant_price.first()
            cart_item_obj.price = variant_pricing.price
            cart_item_obj.discount = variant_pricing.discount
            cart_item_obj.save()
            self.instance = cart_item_obj
            return cart_item_obj

        cart_item = CartItem.objects.create(cart_id=cart_pk, variant_id=variant_pk, **validated_data)
        if cart_item.quantity <= 0:
            cart_item.delete()
            raise serializers.ValidationError('the minimum number of quantity choices product is 1')
        cart_item.save()
        self.instance = cart_item
        return cart_item

class ShowCartItemSerializer(serializers.ModelSerializer):
    cart_total_item = serializers.SerializerMethodField()
    price_after_discount = serializers.SerializerMethodField()
    price_after_tax = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'variant', 'quantity', 'price', 'discount', 'cart_total_item', 'price_after_discount', 'price_after_tax']

    def get_cart_total_item(self, cart_item):
        return cart_item.variant.variant_price.first().price * cart_item.quantity

    def get_price_after_tax(self, cart_item):
        if cart_item.discount:
            return round(
                ((cart_item.price - (cart_item.price * cart_item.discount.amount)) * 1.09) * cart_item.quantity, 2)
        return round((cart_item.price * 1.09) * cart_item.quantity)

    def get_price_after_discount(self, cart_item):
        if cart_item.discount:
            price_after_discount = (cart_item.price - (
                        cart_item.price * cart_item.discount.amount)) * cart_item.quantity
            return price_after_discount
        return cart_item.price * cart_item.quantity

    def get_price(self, instance):
        return instance.price

    def get_discount(self, instance):
        if instance.discount:
            return instance.discount.amount
        return None


class UpdateCartItemSerializer(serializers.ModelSerializer):
    cart_total_item = serializers.SerializerMethodField()
    price_after_discount = serializers.SerializerMethodField()
    price_after_tax = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'variant', 'quantity', 'price', 'discount', 'cart_total_item', 'price_after_discount', 'price_after_tax']

    def get_cart_total_item(self, cart_item):
        return cart_item.variant.variant_price.first().price * cart_item.quantity

    def get_price_after_tax(self, cart_item):
        if cart_item.discount:
            return round(((cart_item.price - (cart_item.price * cart_item.discount.amount)) * 1.09) * cart_item.quantity, 2)
        return round((cart_item.price * 1.09) * cart_item.quantity)

    def get_price_after_discount(self, cart_item):
        if cart_item.discount:
            price_after_discount = (cart_item.price - (cart_item.price * cart_item.discount.amount)) * cart_item.quantity
            return price_after_discount
        return cart_item.price * cart_item.quantity

    def get_price(self, instance):
        return instance.price

    def get_discount(self, instance):
        if instance.discount:
            return instance.discount.amount
        return None

    def update(self, instance, validated_data):
        if 'cart_pk' in self.context:
            cart_pk = self.context['cart_pk']
        else:
            cart_pk = validated_data['cart'].id
            # message = 'dont found any cart-id, please first create a cart and them add cart-items.'
            # raise serializers.ValidationError(detail=message)

        variant_pk = validated_data['variant'].id
        cart = get_object_or_404(Cart, id=cart_pk)
        variant = get_object_or_404(Variant, id=variant_pk)
        quantity = validated_data.get('quantity', 1)

        instance.quantity = quantity
        if instance.quantity <= 0:
            raise serializers.ValidationError('the minimum number of quantity choices product is 1')

        variant_pricing = instance.variant.variant_price.first()
        instance.price = variant_pricing.price
        instance.discount = variant_pricing.discount
        instance.save()
        return instance


class CartSerializer(serializers.ModelSerializer):
    cart_items = ShowCartItemSerializer(many=True, read_only=True, source='items')
    cart_total_price = serializers.SerializerMethodField()
    cart_total_price_after_tax = serializers.SerializerMethodField()
    cart_total_price_after_discount = serializers.SerializerMethodField()


    class Meta:
        model = Cart
        fields = ['id', 'cart_items', 'cart_total_price', 'cart_total_price_after_discount', 'cart_total_price_after_tax']
        read_only_fields = ['id', ]
    # created_at = serializers.DateTimeField()

    def get_cart_total_price(self, cart):
        return sum([item.quantity * item.variant.variant_price.first().price for item in cart.items.all()])

    def get_cart_total_price_after_tax(self, cart):
        total_p_after_t = []
        for item in cart.items.all():
            if item.discount:
                total_price_after_tax = round(((item.price - (item.price * item.discount.amount)) * 1.09) * item.quantity, 2)
                total_p_after_t.append(total_price_after_tax)
            elif item.discount is None:
                total_price_after_tax = round((item.price * 1.09) * item.quantity, 2)
                total_p_after_t.append(total_price_after_tax)
        return sum(total_p_after_t)

    def get_cart_total_price_after_discount(self, cart):
        total_p_after_d = []
        for item in cart.items.all():
            if item.discount:
                total_price_after_discount = (item.price - (item.price * item.discount.amount)) * item.quantity
                total_p_after_d.append(total_price_after_discount)
            elif item.discount is None:
                total_price_after_discount = item.price * item.quantity
                total_p_after_d.append(total_price_after_discount)
        return sum(total_p_after_d)
