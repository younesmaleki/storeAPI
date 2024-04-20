from django_filters.rest_framework import FilterSet

from store.models import Product, Category, Brand, Color, Size, Tag, VariantPricing, Attribute, AttributeValue, Variant, \
    ProductComment, Order, OrderItem, CartItem


class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = {
            'fa_name':['exact', 'contains'],
            'parent': ['exact', ],
            'is_active': ['exact']
        }

class BrandFilter(FilterSet):
    class Meta:
        model = Brand
        fields = {
            'fa_name': ['exact', 'contains'],
            'en_name': ['exact', 'contains']
        }


class ColorFilter(FilterSet):
    class Meta:
        model = Color
        fields = {
            'fa_name': ['exact', 'contains'],
            'en_name': ['exact', 'contains']
        }


class SizeFilter(FilterSet):
    class Meta:
        model = Size
        fields = {
            'title': ['exact', 'contains'],
        }


class TagFilter(FilterSet):
    class Meta:
        model = Tag
        fields = {
            'name': ['exact', 'contains'],
        }


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'fa_name': ['exact', ],
            'en_name': ['exact', 'contains'],
            'category_id': ['exact', ],
            'brand_id': ['exact', ],
            'sizes': ['exact', ],
            'attributes': ['exact', ],
            'gender': ['exact', ],
            'is_active': ['exact', ],
            'tags': ['exact', ],
            'created_at': ['year__lt', 'year__gt'],
            'views': ['gt', 'lt']
        }


class VariantPricingFilter(FilterSet):
    class Meta:
        model = VariantPricing
        fields = {
            'variant_id': ['exact', ],
            'price': ['lt', 'gt', ],
            'discount_id': ['exact', ]
        }

class AttributeValueFilter(FilterSet):
    class Meta:
        model = AttributeValue
        fields = {
            'product_id': ['exact', ],
            'attribute_id': ['exact', ],
            'value': ['contains', ]
        }


class VariantFilter(FilterSet):
    class Meta:
        model = Variant
        fields = {
            'product_id': ['exact', ],
            'color': ['exact', ],
            'size': ['exact', ],
            'inventory': ['lt', 'gt'],
            'is_active': ['exact', ],
        }


class ProductCommentFilter(FilterSet):
    class Meta:
        model = ProductComment
        fields = {
            'product_id': ['exact', ],
            'user_id': ['exact', ],
            'datetime_created': ['year__gt', 'year__lt'],
            'product_stars': ['gt', 'lt'],
        }


class OrderFilter(FilterSet):
    class Meta:
        model = Order
        fields = {
            'customer_id': ['exact', ],
            'status': ['exact', ],
            'created_at': ['year__gt', 'year__lt']
        }

class OrderItemFilter(FilterSet):
    class Meta:
        model = OrderItem
        fields = {
            'order_id': ['exact', ],
            'variant_id': ['exact', ],
            'quantity': ['gt', 'lt'],
            'price': ['gt', 'lt'],
            'discount_id': ['exact', ]
        }


class CartItemFilter(FilterSet):
    class Meta:
        model = CartItem
        fields = {
            'cart_id': ['exact', ],
            'variant_id': ['exact', ],
            'quantity': ['gt', 'lt']
        }