from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from rest_framework import status, mixins, serializers
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from core.models import CustomUser
from store.filters import CategoryFilter, BrandFilter, ColorFilter, SizeFilter, ProductFilter, VariantFilter, \
    AttributeValueFilter, VariantPricingFilter, ProductCommentFilter, OrderFilter, OrderItemFilter, CartItemFilter
from .models import Product, VariantPricing, Order, Category, Brand, Color, Size, AttributeCategory, Attribute, \
    Tag, AttributeValue, Variant, Image, ProductComment, Cart, Address, OrderItem, CartItem, Discount, Customer
from .paginations import DefaultPagination
from .permissions import IsAdminOrReadOnly, SendPrivateEmailToCustomersPermission, CustomDjangoModelPermission
from store.signals import order_created
from .serializers import ProductSerializer, CategorySerializer, \
    BrandSerializer, ColorSerializer, SizeSerializer, AttributeCategorySerializer, TagSerializer, \
    UpdateVariantSerializer, ImageSerializer, CartSerializer, \
    DiscountSerializer, \
    CreateOrderSerializer, CreateAttributeSerializer, CreateAttributeValueSerializer, \
    CreateVariantSerializer, CreateVariantPricingSerializer, \
    ShowAddressSerializer, \
    UpdateAddressSerializer, CreateCustomerAddressSerializer, UpdateAttributeSerializer, ShowAttributeSerializer, \
    ShowAttributeValueSerializer, UpdateAttributeValueSerializer, ShowVariantSerializer, CreateCommentSerializer, \
    ShowCommentSerializer, UpdateVariantPricingSerializer, UpdateOrderSerializer, ShowOrderSerializer, \
    ShowCustomerSerializer, UpdateCustomerSerializer, CreateCustomerSerializer, \
    ShowOrderItemSerializer, CreateCartItemSerializer, UpdateCartItemSerializer, ShowCartItemSerializer, \
    AdminShowOrderSerializer


class CustomerViewSet(ModelViewSet):
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    pagination_class = DefaultPagination
    ordering_fields = ['user__first_name', 'user__last_name']
    filterset_fields = ['user', 'user__first_name', 'user__last_name']
    search_fields = ['user__first_name', 'user__last_name']
    permission_classes = [CustomDjangoModelPermission]

    @action(detail=False, methods=['GET', 'PUT', 'POST', 'DELETE'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        custom_user = get_object_or_404(get_user_model(), id=user.id)
        if request.method == 'GET':
            customer = get_object_or_404(Customer, user_id=user.id)
            serializer = ShowCustomerSerializer(customer)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = CreateCustomerSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response(serializer.data,  status=status.HTTP_201_CREATED)

        elif request.method == 'PUT':
            customer = get_object_or_404(Customer, user_id=user.id)
            serializer = UpdateCustomerSerializer(customer, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        elif request.method == 'DELETE':
            customer = get_object_or_404(Customer, user_id=user.id)
            if customer.order.count() > 0:
                return Response({'errors': 'there is some order including this Customer. Please remove them first.'})
            customer.delete()
            return Response('The object successfully delete it.')

    @action(detail=True, permission_classes=[SendPrivateEmailToCustomersPermission])
    def send_private_email(self, request, pk):
        return Response(f'sending private email to customer : {pk}')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCustomerSerializer
        elif self.request.method in ['PUT', 'PATCH']:
            return UpdateCustomerSerializer
        return ShowCustomerSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        return Customer.objects.select_related('user').prefetch_related('user_address').all()

    def destroy(self, request, pk, *args, **kwargs):
        customer = get_object_or_404(Customer, pk=pk)
        if customer.order.count() > 0:
            return Response({'errors': 'there is some order including this Customer. Please remove them first.'})
        customer.delete()
        return Response({'success': 'This Customer can be deleted.'}, status=status.HTTP_200_OK)



class AddressViewSet(ModelViewSet):
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    pagination_class = DefaultPagination
    ordering_fields = ['customer', 'city']
    search_fields = ['customer', 'city']
    filterset_fields = ['customer', 'city']
    permission_classes = [CustomDjangoModelPermission]

    @action(detail=False, methods=['GET', 'PUT', 'POST', 'DELETE'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        custom_user = get_object_or_404(get_user_model(), id=user.id)
        customer = get_object_or_404(Customer, user_id=user.id)

        if request.method == 'GET':
            address = get_object_or_404(Address, customer_id=customer.id)
            serializer = ShowAddressSerializer(address)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = CreateCustomerAddressSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(customer=customer)  # اضافه کردن فیلد مشتری به سفارش
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'PUT':
            address = get_object_or_404(Address, customer_id=customer.id)
            serializer = UpdateAddressSerializer(address, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(customer=customer)
            return Response(serializer.data)

        elif request.method == 'DELETE':
            address = get_object_or_404(Address, customer_id=customer.id)
            address.delete()
            return Response('The address successfully delete it.')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCustomerAddressSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UpdateAddressSerializer
        return ShowAddressSerializer


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        if 'customer_pk' in self.kwargs:
            context['customer_pk'] = self.kwargs['customer_pk']
        return context

    def get_queryset(self):
        if 'customer_pk' in self.kwargs:
            customer_pk = self.kwargs['customer_pk']
            customer = get_object_or_404(Customer, id=customer_pk)

            return Address.objects.filter(customer_id=customer_pk).all()

        return Address.objects.select_related('customer').all()

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related('products').all()
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    pagination_class = DefaultPagination
    ordering_fields = ['fa_name', 'is_active', 'created_at']
    search_fields = ['fa_name', 'en_name']
    # filterset_fields = ['fa_name', 'parent', 'is_active']
    filterset_class = CategoryFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, pk=pk)

        # بررسی اینکه آیا این دسته بندی والد دارای فرزند است یا خیر
        has_children = category.get_children().exists()

        # اگر دسته بندی والد فرزند دارد
        if has_children:
            children_categories = category.get_children()

            # بررسی هر یک از فرزندها
            for child_category in children_categories:
                # بررسی اینکه آیا فرزند فعلی دارای محصولات است یا خیر
                has_products = child_category.products.exists()
                has_attributes = child_category.attributes.exists()

                # اگر فرزند فعلی دارای محصولات است
                if has_products:
                    return Response({'error': f'Category "{child_category.fa_name}" has associated products.'},
                                    status=status.HTTP_400_BAD_REQUEST)
                if has_attributes:
                    return Response({'error': f'Category "{child_category.fa_name}" has associated attributes.'},
                                    status=status.HTTP_400_BAD_REQUEST)

            category.delete()

        if category.attributes.count() > 0:
            return Response({'errors': "there is some attributes including this category. Please remove them first."})
        if category.products.count() > 0:
            return Response({'errors': "there is some products including this category.Please remove them first"})
        category.delete()

        # اگر هیچ یک از فرزندها محصولاتی ندارند یا اصلا فرزندی ندارند، دسته بندی والد را حذف کنید
        return Response({'success': 'This category can be deleted.'}, status=status.HTTP_200_OK)


class BrandViewSet(ModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['fa_name', 'created_at']
    search_fields = ['fa_name', 'en_name']
    # filterset_fields = ['fa_name',]
    filterset_class = BrandFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, pk, *args, **kwargs):
        brand = get_object_or_404(Brand, pk=pk)
        if brand.products.count() > 0:
            return Response({'errors': 'there is some products including this Brand. Please remove them first.'})
        brand.delete()
        return Response({'success': 'This brand can be deleted.'}, status=status.HTTP_200_OK)


class ColorViewSet(ModelViewSet):
    serializer_class = ColorSerializer
    queryset = Color.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['fa_name', ]
    search_fields = ['fa_name', ]
    # filterset_fields = ['en_name']
    filterset_class = ColorFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, pk, *args, **kwargs):
        color = get_object_or_404(Color, pk=pk)
        if color.products.count() > 0:
            return Response({'errors': 'there is some products including this Color. Please remove them first.'})
        if color.color_variant.count() > 0:
            return Response({'errors': 'there is some variant including this Color.please remove them first.'})
        color.delete()
        return Response({'success': 'This Color can be deleted.'}, status=status.HTTP_200_OK)


class SizeViewSet(ModelViewSet):
    serializer_class = SizeSerializer
    queryset = Size.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['title', ]
    search_fields = ['title', ]
    # filterset_fields = ['title',]
    filterset_class = SizeFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}


    def destroy(self, request, pk, *args, **kwargs):
        size = get_object_or_404(Size, pk=pk)
        if size.variant_size.count() > 0:
            return Response({'errors': 'there is some variant including this Size.please remove them first.'})
        size.delete()
        return Response({'success': 'This Size can be deleted.'}, status=status.HTTP_200_OK)



class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['name', ]
    search_fields = ['name', ]
    filterset_fields = ['name', ]
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['fa_name', 'gender', 'is_active', 'created_at']
    search_fields = ['fa_name', 'en_name', 'category__fa_name', 'category__en_name', 'brand__fa_name',\
                     'short_description', 'model']
    # filterset_fields = ['category_id', 'brand_id', 'sizes', 'attributes', 'gender', 'is_active']
    filterset_class = ProductFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        if 'category_pk' in self.kwargs:
            return {'category_pk': self.kwargs['category_pk']}
        if 'brand_pk' in self.kwargs:
            return {'brand_pk': self.kwargs['brand_pk']}
        else:
            return {'request': self.request}

    def get_queryset(self):

        if 'category_pk' in self.kwargs:
            category_pk = self.kwargs['category_pk']
            category = get_object_or_404(Category, id=category_pk)

            return Product.objects.select_related('category__parent', 'brand').\
                prefetch_related('sizes', 'attributes', 'tags', 'images').\
                filter(category_id=category_pk).all()

        if 'brand_pk' in self.kwargs:
            brand_pk = self.kwargs['brand_pk']
            brand = get_object_or_404(Brand, id=brand_pk)

            return Product.objects.select_related('category__parent', 'brand').\
                prefetch_related('sizes', 'attributes', 'tags', 'images').\
                filter(brand_id=brand_pk).all()

        return Product.objects.select_related('category__parent', 'brand').\
            prefetch_related('sizes', 'attributes', 'tags', 'images').all()

    def destroy(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        if product.attribute_values.count() > 0:
            return Response(
                {'errors': 'there is some attribute values including this product. please first remove them'})
        if product.variants.count() > 0:
            return Response({'errors': 'there is some variant including this product. please first remove them'})
        product.delete()
        return Response({'success': 'This product can be deleted.'}, status=status.HTTP_200_OK)


class VariantPriceViewSet(ModelViewSet):
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['variant', 'price', 'discount']
    search_fields = ['variant__product__fa_name', 'variant__product__en_name', 'price']
    # filterset_fields = ['variant_id', 'price', 'discount_id']
    filterset_class = VariantPricingFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateVariantPricingSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UpdateVariantPricingSerializer
        return UpdateVariantPricingSerializer


    def get_serializer_context(self):
        if 'variant_pk' in self.kwargs:
            return {'variant_pk': self.kwargs['variant_pk']}
        else:
            return {'request': self.request}

    def get_queryset(self):
        if 'variant_pk' in self.kwargs:
            variant_pk = self.kwargs['variant_pk']
            variant = get_object_or_404(Variant, id=variant_pk)

            return VariantPricing.objects.select_related('variant', 'discount').filter(variant_id=variant_pk).all()

        return VariantPricing.objects.select_related('variant', 'discount').all()


class DiscountViewSet(ModelViewSet):
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['amount', ]
    search_fields = ['amount', ]
    filterset_fields = ['amount']
    permission_classes = [IsAdminOrReadOnly]

class AttributeCategoryViewSet(ModelViewSet):
    serializer_class = AttributeCategorySerializer
    queryset = AttributeCategory.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['fa_name', 'created_at', ]
    search_fields = ['fa_name', ]
    filterset_fields = ['fa_name', ]
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}


    def destroy(self, request, pk, *args, **kwargs):
        attribute_category = get_object_or_404(AttributeCategory, pk=pk)
        if attribute_category.single_attribute.count() > 0:
            return Response(
                {'errors': 'there is some attribute including this attribute category.please remove them first.'})
        attribute_category.delete()
        return Response({'success': 'This attribute category can be deleted.'}, status=status.HTTP_200_OK)



class AttributeViewSet(ModelViewSet):
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['fa_name', 'attribute_category', 'created_at']
    search_fields = ['fa_name', ]
    filterset_fields = ['fa_name', 'categories', 'attribute_category_id']
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateAttributeSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UpdateAttributeSerializer
        return ShowAttributeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request

        if 'attribute_category_pk' in self.kwargs:
            context['attribute_category_pk'] = self.kwargs['attribute_category_pk']
        return context

    def get_queryset(self):
        if 'attribute_category_pk' in self.kwargs:
            attribute_category_pk = self.kwargs['attribute_category_pk']
            attribute_category = get_object_or_404(AttributeCategory, id=attribute_category_pk)

            return Attribute.objects.filter(attribute_category_id=attribute_category_pk).all()

        return Attribute.objects.select_related('attribute_category').prefetch_related('categories').all()

    def destroy(self, request, pk, *args, **kwargs):
        attribute = get_object_or_404(Attribute, pk=pk)
        if attribute.value.count() > 0:
            return Response(
                {'errors': 'there is some attribute values including this attribute. please remove them first.'})
        attribute.delete()
        return Response({'success': 'This attribute can be deleted.'}, status=status.HTTP_200_OK)



class AttributeValueViewSet(ModelViewSet):
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['attribute', 'created_at']
    search_fields = ['value', ]
    # filterset_fields = ['product_id', 'attribute_id']
    filterset_class = AttributeValueFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateAttributeValueSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UpdateAttributeValueSerializer
        return ShowAttributeValueSerializer

    def get_serializer_context(self):
        if 'attribute_pk' in self.kwargs:
            return {'attribute_pk': self.kwargs['attribute_pk']}
        else:
            return {'request': self.request}

    def get_queryset(self):
        if 'attribute_pk' in self.kwargs:
            attribute_pk = self.kwargs['attribute_pk']
            attribute = get_object_or_404(Attribute, id=attribute_pk)

            return AttributeValue.objects.select_related('product', 'attribute').filter(attribute_id=attribute_pk).all()

        return AttributeValue.objects.select_related('product', 'attribute').all()


class VariantViewSet(ModelViewSet):
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['color', 'size', 'inventory', 'is_active']
    search_fields = ['product__fa_name', 'product__en_name', ]
    # filterset_fields = ['product_id', 'color_id', 'size_id', 'inventory', 'is_active']
    filterset_class = VariantFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateVariantSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UpdateVariantSerializer
        return ShowVariantSerializer


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        if 'product_pk' in self.kwargs:
            context['product_pk']= self.kwargs['product_pk']
        return context


    def get_queryset(self):
        if 'product_pk' in self.kwargs:
            product_pk = self.kwargs['product_pk']
            product = get_object_or_404(Product, id=product_pk)

            return Variant.objects.filter(product_id=product_pk).all()

        return Variant.objects.select_related('product', 'color', 'size').all()


class ImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.prefetch_related('products').all()
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['product', 'created_at']
    search_fields = ['products__fa_name', 'products__en_name', ]
    permission_classes = [IsAdminOrReadOnly]


class CommentViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['product', 'user', 'datetime_created', 'product_stars', 'comment_status']
    search_fields = ['body',]
    # filterset_fields = ['product_id', 'user_id', 'datetime_created', 'product_stars', ]
    filterset_class = ProductCommentFilter
    permission_classes = [IsAuthenticatedOrReadOnly]


    def get_serializer_class(self):
        if 'product_pk' in self.kwargs:
            if self.request.method == 'POST':
                return CreateCommentSerializer
            elif self.request.method == 'GET':
                return ShowCommentSerializer
            # elif self.request.method == 'DELETE':
            #     return DeleteCommentSerializer

    def destroy(self, request, pk, *args, **kwargs):
        comment_obj = get_object_or_404(ProductComment, pk=pk)
        user = request.user
        if comment_obj.user.id == user.id:
            comment_obj.delete()
            return Response('the comment successfully delete it by user.')
        elif user.is_staff:
            comment_obj.delete()
            return Response('the comment successfully delete it by admin user.')
        else:
            message = 'you has not permission for delete this comment'
            raise serializers.ValidationError(detail=message)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        if 'product_pk' in self.kwargs:
            context['product_pk']= self.kwargs['product_pk']
        return context


    def get_queryset(self, **kwargs):
        if 'product_pk' in self.kwargs:
            product_pk = self.kwargs['product_pk']
            product = get_object_or_404(Product, id=product_pk)

            return ProductComment.objects.filter(product_id=product_pk).all()

        return ProductComment.objects.select_related('product').all()



class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['customer', 'status', 'created_at']
    search_fields = ['customer__first_name', 'customer__last_name', 'address']
    # filterset_fields = ['customer_id', 'status', 'created_at']
    filterset_class = OrderFilter
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    def me(self, request):

        user_id = request.user.id
        customer = get_object_or_404(Customer, user_id=user_id)

        if request.method == 'GET':
            # order = get_object_or_404(Order, customer_id=customer.id)
            if Order.objects.filter(customer_id=customer.id).exists():
                orders = Order.objects.filter(customer_id=customer.id)
                serializer = ShowOrderSerializer(orders, many=True)
            else:
                order = get_object_or_404(Order, customer_id=customer.id)
                serializer = ShowOrderSerializer(order)

            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = CreateOrderSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            order_created = serializer.save()  # اضافه کردن فیلد مشتری به سفارش
            serializer = ShowOrderSerializer(order_created)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get_permissions(self):
        if self.request.method in ['PATCH', 'Delete']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        elif self.request.method == 'GET' and self.request.user.is_staff:
            return AdminShowOrderSerializer
        return ShowOrderSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        if 'customer_pk' in self.kwargs:
            context['customer_pk'] = self.kwargs['customer_pk']
        return context


    def get_queryset(self):
        queryset = Order.objects.select_related('customer').prefetch_related('items').all()

        if self.request.user.is_staff:
            if 'customer_pk' in self.kwargs:
                customer_pk = self.kwargs['customer_pk']
                customer = get_object_or_404(Customer, id=customer_pk)

                return Order.objects.filter(customer_id=customer_pk).all()
            else:
                return queryset

        return queryset.filter(customer__user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        create_order_serializer = CreateOrderSerializer(data=request.data, context={'request': self.request})
        create_order_serializer.is_valid(raise_exception=True)
        created_order = create_order_serializer.save()
        order_created.send_robust(self.__class__, order=created_order)
        serializer = ShowOrderSerializer(created_order)
        return Response(serializer.data)


class OrderItemViewSet(ModelViewSet):
    http_method_names = ['get', 'delete']
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['variant', 'quantity', 'price']
    search_fields = ['variant__product__fa_name', 'variant__product__en_name', ]
    # filterset_fields = ['order_id', 'variant_id', 'price']
    filterset_class = OrderItemFilter
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return ShowOrderItemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


    def get_queryset(self):
        queryset =  OrderItem.objects.\
            select_related('order__customer__user',
                           'variant__color',
                           'variant__product__category',
                           'variant__product__brand').\
            prefetch_related(Prefetch(
                                'variant',
                                queryset=Variant.objects.select_related('Product__brand'),
                            )).all()

        if self.request.user.is_staff:
            return queryset
        return queryset.filter(order__customer__user_id=self.request.user.id)


class CartViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', ]
    lookup_value_regex = '[0-9a-fA-F]{8}\-?[0-9a-fA-F]{4}\-?[0-9a-fA-F]{4}\-?[0-9a-fA-F]{4}\-?[0-9a-fA-F]{12}'
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'options', 'head']
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['cart', 'variant', 'quantity']
    search_fields = ['variant__product__fa_name', 'variant__product__en_name']
    # filterset_fields = ['cart_id', 'variant_id', ]
    filterset_class = CartItemFilter
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCartItemSerializer
        elif self.request.method in ['PUT', 'PATCH']:
            return UpdateCartItemSerializer
        return ShowCartItemSerializer

    def get_serializer_context(self):
        if 'cart_pk' in self.kwargs:
            return {'cart_pk': self.kwargs['cart_pk']}
        return {'request': self.request}

    def get_queryset(self):
        if 'cart_pk' in self.kwargs:
            cart_pk = self.kwargs['cart_pk']
            cart = get_object_or_404(Cart, id=cart_pk)

            return CartItem.objects.select_related('variant').filter(cart_id=cart_pk).all()

        return CartItem.objects.select_related('cart', 'variant').all()

