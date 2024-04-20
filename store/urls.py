from django.conf.urls.static import static
from django.urls import path
from rest_framework_nested import routers
from rest_framework.routers import SimpleRouter, DefaultRouter

from config import settings
from . import views

router = DefaultRouter()
router.register('customers', views.CustomerViewSet, basename='customer')
router.register('address', views.AddressViewSet, basename='address')
router.register('category', views.CategoryViewSet, basename='category')
router.register('brands', views.BrandViewSet, basename='brand')
router.register('colors', views.ColorViewSet, basename='color')
router.register('sizes', views.SizeViewSet, basename='size')
router.register('attributes_category', views.AttributeCategoryViewSet, basename='attribute-category')
router.register('attribute', views.AttributeViewSet, basename='attribute')
router.register('tags', views.TagViewSet, basename='tag')
router.register('products', views.ProductViewSet, basename='product')
router.register('discounts', views.DiscountViewSet, basename='discount')
router.register('variant_prices', views.VariantPriceViewSet, basename='product-price')
router.register('attribute_value', views.AttributeValueViewSet, basename='attribute-value')
router.register('variants', views.VariantViewSet, basename='variant')
router.register('images', views.ImageViewSet, basename='image')
router.register('orders', views.OrderViewSet, basename='order')
router.register('order_items', views.OrderItemViewSet, basename='order-items')
router.register('carts', views.CartViewSet, basename='cart')
router.register('cart_items', views.CartItemViewSet, basename='cart-items')

customer_orders_router = routers.NestedDefaultRouter(router, 'customers', lookup='customer')
customer_orders_router.register('orders', views.OrderViewSet, basename='customer-orders')

customer_addresses_router = routers.NestedDefaultRouter(router, 'customers', lookup='customer')
customer_addresses_router.register('addresses', views.AddressViewSet, basename='customers-address')

products_category_router = routers.NestedDefaultRouter(router, 'category', lookup='category')
products_category_router.register('products', views.ProductViewSet, basename='products-category')

products_brand_router = routers.NestedDefaultRouter(router, 'brands', lookup='brand')
products_brand_router.register('products', views.ProductViewSet, basename='products-brand')

attributes_category_attribute_router = routers.NestedDefaultRouter(router, 'attributes_category', lookup='attribute_category')
attributes_category_attribute_router.register('attributes', views.AttributeViewSet, basename='attributes')

attribute_attribute_value_router = routers.NestedDefaultRouter(router, 'attribute', lookup='attribute')
attribute_attribute_value_router.register('attribute_value', views.AttributeValueViewSet, basename='attribute-values')

product_variants_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_variants_router.register('variants', views.VariantViewSet, basename='product-variants')

product_comments_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_comments_router.register('comments', views.CommentViewSet, basename='product-comments')

variant_prices_router = routers.NestedDefaultRouter(router, 'variants', lookup='variant')
variant_prices_router.register('prices', views.VariantPriceViewSet, basename='variant-prices')

cart_cart_items_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_cart_items_router.register('cart_items', views.CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + product_comments_router.urls + customer_addresses_router.urls + attributes_category_attribute_router.urls \
              + products_category_router.urls + cart_cart_items_router.urls + attribute_attribute_value_router.urls \
              + customer_orders_router.urls + variant_prices_router.urls \
              + product_variants_router.urls \
              + products_brand_router.urls

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#
# # urlpatterns = [
# #     path('customer_list/', views.CustomerList.as_view(), name='customer-list'),
# #     path('customer_detail/<int:pk>/', views.CustomerDetail.as_view(), name='customer-detail'),
# #     path('address_list/', views.AddressList.as_view(), name='address-list'),
# #     path('address_detail/<int:pk>/', views.AddressDetail.as_view(), name='address-detail'),
# #     path('category_list/', views.CategoryList.as_view(), name='category-list'),
# #     path('category_detail/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
# #     path('brand_list/', views.BrandList.as_view(), name='brand-list'),
# #     path('brand_detail/<int:pk>/', views.BrandDetail.as_view(), name='brand-detail'),
# #     path('size_list/', views.SizeList.as_view(), name='size-list'),
# #     path('size_detail/<int:pk>/', views.SizeDetail.as_view(), name='size-detail'),
# #     path('attribute_category_list/', views.AttributeCategoryList.as_view(), name='attribute-category-list'),
# #     path('attribute_category_detail/<int:pk>/', views.AttributeCategoryDetail.as_view(), name='attribute-category-detail'),
# #     path('attribute_list/', views.AttributeList.as_view(), name='attribute-list'),
# #     path('attribute_detail/<int:pk>/', views.AttributeDetail.as_view(), name='attribute-detail'),
# #     path('tag_list/', views.TagList.as_view(), name='tag-list'),
# #     path('tag_detail/<int:pk>/', views.TagDetail.as_view(), name='tag-detail'),
# #     path('product_list/', views.ProductList.as_view(), name='product-list'),
# #     path('product_detail/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
# #     path('product_price_list/', views.ProductPriceList.as_view(), name='product-price-list'),
# #     path('product_price_detail/<int:pk>/', views.ProductPriceDetail.as_view(), name='product-price-detail'),
# #     path('attribute_value_list/', views.AttributeValueList.as_view(), name='attribute-value-list'),
# #     path('attribute_value_detail/<int:pk>/', views.AttributeValueDetail.as_view(), name='attribute-value-detail'),
# #     path('variant_list/', views.VariantList.as_view(), name='variant-list'),
# #     path('varinat_detail/<int:pk>/', views.VariantDetail.as_view(), name='variant-detail'),
# #     path('image_list/', views.ImageList.as_view(), name='image-list'),
# #     path('image_detail/<int:pk>/', views.ImageDetail.as_view(), name='image-detail'),
# #     path('product_comment_list/', views.ProductCommentList.as_view(), name='product-comment-list'),
# #     path('product_comment_detail/<int:pk>/', views.ProductCommentDetail.as_view(), name='product-comment-detail'),
# #     path('order_list/<int:pk>/', views.OrderList.as_view(), name='order-list'),
# #     path('order_detail/<int:pk>/', views.OrderDetail.as_view(), name='order-detail'),
# #     path('order_item_list/', views.OrderItemList.as_view(), name='order-item-list'),
# #     path('order_item_detail/<int:pk>/', views.OrderItemDetail.as_view(), name='order-item-detail'),
# #     path('cart_list/', views.CartList.as_view(), name='cart-list'),
# #     path('cart_detail/<int:pk>/', views.CartDetail.as_view(), name='cart-detail'),
# #     path('cart_item_list/', views.CartItemList.as_view(), name='cart-item-list'),
# #     path('cart_item_detail/<int:pk>/', views.CartItemDetail.as_view(), name='cart-item-detail'),
# # ]
