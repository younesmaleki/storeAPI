# class CustomerList(ListCreateAPIView):
#     serializer_class = CustomerSerializer
#     queryset = Customer.objects.all()
#
#     # def get_serializer_class(self):
#     #     return  CustomerSerializer
#
#     # def get_queryset(self):
#     #     return Customer.objects.all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#
# class CustomerDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = CustomerSerializer
#     queryset = Customer.objects.all()


# class CustomerList(APIView):
#     def get(self, request):
#         customer_queryset = Customer.objects.all()
#         serializer = CustomerSerializer(customer_queryset, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = CustomerSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# class CustomerDetail(APIView):
#     def get(self, request, pk):
#         customer = get_object_or_404(Customer, pk=pk)
#         serializer = CustomerSerializer(customer)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         customer = get_object_or_404(Customer, pk=pk)
#         serializer = CustomerSerializer(customer, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         customer = get_object_or_404(Customer, pk=pk)
#         customer.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def customer_list(request):
#     if request.method == 'GET':
#         customer_queryset = Customer.objects.all()
#         serializer = CustomerSerializer(customer_queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CustomerSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# @api_view(['GET', 'PUT', 'DELETE'])
# def customer_detail(request, pk):
#     customer = get_object_or_404(Customer, pk=pk)
#     if request.method == 'GET':
#         serializer = CustomerSerializer(customer)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CustomerSerializer(customer, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,)
#     elif request.method == 'DELETE':
#         customer.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# class AddressList(ListCreateAPIView):
#     serializer_class = AddressSerializer
#     queryset = Address.objects.select_related('customer').all()
#
#     # def get_serializer_class(self):
#     #     return AddressSerializer
#
#     # def get_queryset(self):
#     #     return Address.objects.select_related('customer').all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#
# class AddressDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = AddressSerializer
#     queryset = Address.objects.all()


# class AddressList(APIView):
#     def get(self, request):
#         address_queryset = Address.objects.select_related('customer').all()
#         serializer = AddressSerializer(address_queryset, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = AddressSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# class AddressDetail(APIView):
#     def get(self, request, pk):
#         address = get_object_or_404(Address, pk=pk)
#         serializer = AddressSerializer(address)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         address = get_object_or_404(Address, pk=pk)
#         serializer = AddressSerializer(address, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         address = get_object_or_404(Address, pk=pk)
#         address.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def address_list(request):
#     if request.method == 'GET':
#         address_queryset = Address.objects.select_related('customer').all()
#         serializer = AddressSerializer(address_queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = AddressSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# @api_view(['GET', 'PUT', 'DELETE'])
# def address_detail(request, pk):
#     address = get_object_or_404(Address, pk=pk)
#     if request.method == 'GET':
#         serializer = AddressSerializer(address)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = AddressSerializer(address, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         address.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# class CategoryList(ListCreateAPIView):
#     serializer_class = CategorySerializer
#     queryset = Category.objects.prefetch_related('products').all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#
# class CategoryDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = CategorySerializer
#     queryset = Category.objects.prefetch_related('products', 'parent').all()
#
#     def delete(self, request, pk, *args, **kwargs):
#         category = get_object_or_404(Category, pk=pk)
#         if category.attributes.count() > 0:
#             return Response({'errors': "there is some attributes including this category. Please remove them first."})
#         if category.products.count() > 0:
#             return Response({'errors': "there is some products including this category.Please remove them first"})
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class CategoryList(APIView):
#     def get(self, request):
#         category_queryset = Category.objects.prefetch_related('products').all()
#         serializer = CategorySerializer(category_queryset, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = CategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('category list is posting.')


# class CategoryDetail(APIView):
#     def get(self, request, pk):
#         category = get_object_or_404(Category, pk=pk)
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         category = get_object_or_404(Category, pk=pk)
#         serializer = CategorySerializer(category, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

# def delete(self, request, pk):
#     category = get_object_or_404(Category, pk=pk)
#     if category.attributes.count() > 0:
#         return Response({'errors': "there is some attributes including this category. Please remove them first."})
#     if category.products.count() > 0:
#         return Response({'errors': "there is some products including this category.Please remove them first"})
#     category.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def category_list(request):
#     if request.method == 'GET':
#         category_queryset = Category.objects.all()
#         serializer = CategorySerializer(category_queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('category list is posting.')


# @api_view(['GET', 'PUT', 'DELETE'])
# def category_detail(request, pk):
#     category = get_object_or_404(Category, pk=pk)
#     if request.method == 'GET':
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CategorySerializer(category, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if category.attributes.count() > 0:
#             return Response({'errors': "there is some attributes including this category. Please remove them first."})
#         if category.products.count() > 0:
#             return Response({'errors': "there is some products including this category.Please remove them first"})
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# class BrandList(ListCreateAPIView):
#     serializer_class = BrandSerializer
#     queryset = Brand.objects.all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
# class BrandDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = BrandSerializer
#     queryset = Brand.objects.all()
#
#     def delete(self, request, pk, *args, **kwargs):
#         brand = get_object_or_404(Brand, pk=pk)
#         if brand.products.count() > 0:
#             return Response({'errors': 'there is some products including this Brand. Please remove them first.'})
#         brand.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class BrandList(APIView):
#     def get(self, request):
#         brand_queryset = Brand.objects.all()
#         serializer = BrandSerializer(brand_queryset, many=True )
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = BrandSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('brand list is posting.')


# class BrandDetail(APIView):
#     def get(self, request, pk):
#         brand = get_object_or_404(Brand, pk=pk)
#         serializer = BrandSerializer(brand)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         brand = get_object_or_404(Brand, pk=pk)
#         serializer = BrandSerializer(brand, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

# def delete(self, request, pk):
#     brand = get_object_or_404(Brand, pk=pk)
#     if brand.products.count() > 0:
#         return Response({'errors': 'there is some products including this Brand. Please remove them first.'})
#     brand.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def brand_list(request):
#     if request.method == 'GET':
#         brand_queryset = Brand.objects.all()
#         serializer = BrandSerializer(brand_queryset, many=True )
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = BrandSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('brand list is posting.')


# @api_view(['GET', 'PUT', 'DELETE'])
# def brand_detail(request, pk):
#     brand = get_object_or_404(Brand, pk=pk)
#     if request.method == 'GET':
#         serializer = BrandSerializer(brand)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = BrandSerializer(brand, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if brand.products.count() > 0:
#             return Response({'errors': 'there is some products including this Brand. Please remove them first.'})
#         brand.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# class ColorList(ListCreateAPIView):
#     serializer_class = ColorSerializer
#     queryset = Color.objects.all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#
# class ColorDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = ColorSerializer
#     queryset = Color.objects.all()
#
#     def delete(self, request, pk, *args, **kwargs):
#         color = get_object_or_404(Color, pk=pk)
#         if color.products.count() > 0:
#             return Response({'errors': 'there is some products including this Color. Please remove them first.'})
#         if color.color_price.count() > 0:
#             return Response({'errors': 'there is some product price including this Color.please remove them first.'})
#         if color.color_variant.count() > 0:
#             return Response({'errors': 'there is some variant including this Color.please remove them first.'})
#         color.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ColorList(APIView):
#     def get(self, request):
#         color_queryset = Color.objects.all()
#         serializer = ColorSerializer(color_queryset, many=True)
#         return Response(serializer.data)
#     def post(self, request):
#         serializer = ColorSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('color list is posting.')


# class ColorDetail(APIView):
#     def get(self, request, pk):
#         color = get_object_or_404(Color, pk=pk)
#         serializer = ColorSerializer(color)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         color = get_object_or_404(Color, pk=pk)
#         serializer = ColorSerializer(color, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

# def delete(self, request, pk):
#     color = get_object_or_404(Color, pk=pk)
#     if color.products.count() > 0:
#         return Response({'errors': 'there is some products including this Color. Please remove them first.'})
#     if color.color_price.count() > 0:
#         return Response({'errors': 'there is some product price including this Color.please remove them first.'})
#     if color.color_variant.count() > 0:
#         return Response({'errors': 'there is some variant including this Color.please remove them first.'})
#     color.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def color_list(request):
#     if request.method == 'GET':
#         color_queryset = Color.objects.all()
#         serializer = ColorSerializer(color_queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ColorSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('color list is posting.')


# @api_view(['GET', 'PUT', 'DELETE'])
# def color_detail(request, pk):
#     color = get_object_or_404(Color, pk=pk)
#     if request.method == 'GET':
#         serializer = ColorSerializer(color)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ColorSerializer(color, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if color.products.count() > 0:
#             return Response({'errors': 'there is some products including this Color. Please remove them first.'})
#         if color.color_price.count() > 0:
#             return Response({'errors': 'there is some product price including this Color.please remove them first.'})
#         if color.color_variant.count() > 0:
#             return Response({'errors': 'there is some variant including this Color.please remove them first.'})
#         color.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# class SizeList(ListCreateAPIView):
#     serializer_class = SizeSerializer
#     queryset = Size.objects.all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#
# class SizeDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = SizeSerializer
#     queryset = Size.objects.all()
#
#     def delete(self, request, pk, *args, **kwargs):
#         size = get_object_or_404(Size, pk=pk)
#         if size.varaint_size.count() > 0:
#             return Response({'errors': 'there is some variant including this Size.please remove them first.'})
#         size.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class SizeList(APIView):
#     def get(self, request):
#         size_queryset = Size.objects.all()
#         serializer = SizeSerializer(size_queryset, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = SizeSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('size list is posting.')


# class SizeDetail(APIView):
#     def get(self, request, pk):
#         size = get_object_or_404(Size, pk=pk)
#         serializer = SizeSerializer(size)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         size = get_object_or_404(Size, pk=pk)
#         serializer = SizeSerializer(size, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         size = get_object_or_404(Size, pk=pk)
#         if size.varaint_size.count() > 0:
#             return Response({'errors': 'there is some variant including this Size.please remove them first.'})
#         size.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def size_list(request):
#     if request.method == 'GET':
#         size_queryset = Size.objects.all()
#         serializer = SizeSerializer(size_queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = SizeSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('size list is posting.')
#


# @api_view(['GET', 'PUT', 'DELETE'])
# def size_detail(request, pk):
#     size = get_object_or_404(Size, pk=pk)
#     if request.method == 'GET':
#         serializer = SizeSerializer(size)
#         return Response(serializer.data)
#     if request.method == 'PUT':
#         serializer = SizeSerializer(size, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     if request.method == 'DELETE':
#         if size.varaint_size.count() > 0:
#             return Response({'errors': 'there is some variant including this Size.please remove them first.'})
#         size.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class AttributeCategoryList(ListCreateAPIView):
#     serializer_class = AttributeCategorySerializer
#     queryset = AttributeCategory.objects.all()
#
#     def get_content_negotiator(self):
#         return {'request': self.request}
#
#
# class AttributeCategoryDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = AttributeCategorySerializer
#     queryset = AttributeCategory.objects.all()
#
#     def delete(self, request, pk, *args, **kwargs):
#         attribute_category = get_object_or_404(AttributeCategory, pk=pk)
#         if attribute_category.single_attribute.count() > 0:
#             return Response(
#                 {'errors': 'there is some attribute including this attribute category.please remove them first.'})
#         attribute_category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class AttributeCategoryList(APIView):
#     def get(self, request):
#         attribute_category_queryset = AttributeCategory.objects.all()
#         serializer = AttributeCategorySerializer(attribute_category_queryset, many=True)
#         return Response(serializer.data)
#     def post(self, request):
#         serializer = AttributeCategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('attribute category list is posting.')


# class AttributeCategoryDetail(APIView):
#     def get(self, request, pk):
#         attribute_category = get_object_or_404(AttributeCategory, pk=pk)
#         serializer = AttributeCategorySerializer(attribute_category)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         attribute_category = get_object_or_404(AttributeCategory, pk=pk)
#         serializer = AttributeCategorySerializer(attribute_category, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         attribute_category = get_object_or_404(AttributeCategory, pk=pk)
#         if attribute_category.single_attribute.count() > 0:
#             return Response(
#                 {'errors': 'there is some attribute including this attribute category.please remove them first.'})
#         attribute_category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def attribute_category_list(request):
#     if request.method == 'GET':
#         attribute_category_queryset = AttributeCategory.objects.all()
#         serializer = AttributeCategorySerializer(attribute_category_queryset, many=True)
#         return Response(serializer.data)
#     if request.method == 'POST':
#         serializer = AttributeCategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('attribute category list is posting.')


# @api_view(['GET', 'PUT', 'DELETE'])
# def attribute_category_detail(request, pk):
#     attribute_category = get_object_or_404(AttributeCategory, pk=pk)
#     if request.method == 'GET':
#         serializer = AttributeCategorySerializer(attribute_category)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = AttributeCategorySerializer(attribute_category, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if attribute_category.single_attribute.count() > 0:
#             return Response({'errors': 'there is some attribute including this attribute category.please remove them first.'})
#         attribute_category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# class AttributeList(ListCreateAPIView):
#     serializer_class = AttributeSerializer
#     queryset = Attribute.objects.select_related('category', 'attribute_category').all()
#
#     def get_content_negotiator(self):
#         return {'request': self.request}
#
#
# class AttributeDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = AttributeSerializer
#     queryset = Attribute.objects.all()
#
#     def delete(self, request, pk, *args, **kwargs):
#         attribute = get_object_or_404(Attribute, pk=pk)
#         if attribute.value.count() > 0:
#             return Response(
#                 {'errors': 'there is some attribute including this attribute values.please remove them first.'})
#         attribute.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class AttributeList(APIView):
#     def get(self, request):
#         attribute_queryset = Attribute.objects.select_related('category', 'attribute_category').all()
#         serializer = AttributeSerializer(attribute_queryset, many=True)
#         return Response(serializer.data)
#     def post(self, request):
#         serializer = AttributeSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('attribute list is posting')


# class AttributeDetail(APIView):
#     def get(self, request, pk):
#         attribute = get_object_or_404(Attribute, pk=pk)
#         serializer = AttributeSerializer(attribute)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         attribute = get_object_or_404(Attribute, pk=pk)
#         serializer = AttributeSerializer(attribute, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         attribute = get_object_or_404(Attribute, pk=pk)
#         if attribute.value.count() > 0:
#             return Response(
#                 {'errors': 'there is some attribute including this attribute values.please remove them first.'})
#         attribute.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def attribute_list(request):
#     if request.method == 'GET':
#         attribute_queryset = Attribute.objects.select_related('category', 'attribute_category').all()
#         serializer = AttributeSerializer(attribute_queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = AttributeSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('attribute list is posting')


# @api_view(['GET', 'PUT', 'DELETE'])
# def attribute_detail(request, pk):
#     attribute = get_object_or_404(Attribute, pk=pk)
#     if request.method == 'GET':
#         serializer = AttributeSerializer(attribute)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = AttributeSerializer(attribute, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if attribute.value.count() > 0:
#             return Response({'errors': 'there is some attribute including this attribute values.please remove them first.'})
#         attribute.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# class TagList(ListCreateAPIView):
#     serializer_class = TagSerializer
#     queryset = Tag.objects.all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#
# class TagDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = TagSerializer
#     queryset = Tag.objects.all()


# class TagList(APIView):
#     def get(self, request):
#         tag_queryset = Tag.objects.all()
#         serializer = TagSerializer(tag_queryset, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = TagSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('tag list is posting.')


# class TagDetail(APIView):
#     def get(self, request, pk):
#         tag = get_object_or_404(Tag, pk=pk)
#         serializer = TagSerializer(tag)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         tag = get_object_or_404(Tag, pk=pk)
#         serializer = TagSerializer(tag, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         tag = get_object_or_404(Tag, pk=pk)
#         tag.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def tag_list(request):
#     if request.method == 'GET':
#         tag_queryset = Tag.objects.all()
#         serializer = TagSerializer(tag_queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = TagSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('tag list is posting.')


# @api_view(['GET', 'PUT', 'DELETE'])
# def tag_detail(request, pk):
#     tag = get_object_or_404(Tag, pk=pk)
#     if request.method == 'GET':
#         serializer = TagSerializer(tag)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = TagSerializer(tag, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         tag.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# class ProductList(ListCreateAPIView):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.select_related('category__parent', 'brand').prefetch_related('colors', 'sizes',
#                                                                                             'attribute', 'tags').all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()
#
#     def delete(self, request, pk, *args, **kwargs):
#         product = get_object_or_404(Product, pk=pk)
#         if product.price.count() > 0:
#             return Response({'errors': 'there is some product price including this product.please first remove them'})
#         if product.attribute_values.count() > 0:
#             return Response(
#                 {'errors': 'there is some attribute values including this product. please first remove them'})
#         if product.variant.count() > 0:
#             return Response({'errors': 'there is some variant including this product. please first remove them'})
#         if product.images.count() > 0:
#             return Response({'errors': 'there is some image including this product. please first remove them.'})
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ProductList(APIView):
#     def get(self, request):
#         product_queryset = Product.objects.select_related('category__parent', 'brand').prefetch_related('colors', 'sizes', 'attribute', 'tags').all()
#         serializer = ProductSerializer(product_queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#
#     def post(self, request, pk):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('product list is posting')


# class ProductDetail(APIView):
#     def get(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         serializer = ProductSerializer(product, context={'request': request})
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.price.count() > 0:
#             return Response({'errors': 'there is some product price including this product.please first remove them'})
#         if product.attribute_values.count() > 0:
#             return Response(
#                 {'errors': 'there is some attribute values including this product. please first remove them'})
#         if product.variant.count() > 0:
#             return Response({'errors': 'there is some variant including this product. please first remove them'})
#         if product.images.count() > 0:
#             return Response({'errors': 'there is some image including this product. please first remove them.'})
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         product_queryset = Product.objects.select_related('category__parent', 'brand').prefetch_related('colors', 'sizes', 'attribute', 'tags').all()
#         serializer = ProductSerializer(product_queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('product list is posting')


# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if product.price.count() > 0:
#             return Response({'errors': 'there is some product price including this product.please first remove them'})
#         if product.attribute_values.count() > 0:
#             return Response({'errors': 'there is some attribute values including this product. please first remove them'})
#         if product.variant.count() > 0:
#             return Response({'errors': 'there is some variant including this product. please first remove them'})
#         if product.images.count() > 0:
#             return Response({'errors': 'there is some image including this product. please first remove them.'})
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# class ProductPriceList(ListCreateAPIView):
#     serializer_class = VariantPricingSerializer
#     queryset = VariantPricing.objects.select_related('product', 'color').prefetch_related('discount').all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#
# class ProductPriceDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = VariantPricingSerializer
#     queryset = VariantPricing.objects.all()


# class ProductPriceList(APIView):
#     def get(self, request):
#         product_pricing_queryset = VariantPricing.objects.select_related('product', 'color').prefetch_related('discount').all()
#         serializer = VariantPricingSerializer(product_pricing_queryset, many=True)
#         return Response(serializer.data)
#     def post(self, request):
#         serializer = VariantPricingSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('product pricing list is posting')

# class ProductPriceDetail(APIView):
#     def get(self, request, pk):
#         product_price = get_object_or_404(VariantPricing, pk=pk)
#         serializer = VariantPricingSerializer(product_price)
#         return Response(serializer.data)
#     def put(self, request, pk):
#         product_price = get_object_or_404(VariantPricing, pk=pk)
#         serializer = VariantPricingSerializer(product_price, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     def delete(self, request, pk):
#         product_price = get_object_or_404(VariantPricing, pk=pk)
#         product_price.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def product_price_list(request):
#     if request.method == 'GET':
#         product_pricing_queryset = VariantPricing.objects.select_related('product', 'color').prefetch_related('discount').all()
#         serializer = VariantPricingSerializer(product_pricing_queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = VariantPricingSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('product pricing list is posting')


# @api_view(['GET', 'PUT', 'DELETE'])
# def product_price_detail(request, pk):
#     product_price = get_object_or_404(VariantPricing, pk=pk)
#     if request.method == 'GET':
#         serializer = VariantPricingSerializer(product_price)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = VariantPricingSerializer(product_price, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         product_price.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class AttributeValueList(ListCreateAPIView):
#     serializer_class = AttributeValueSerializer
#     queryset = AttributeValue.objects.select_related('product', ' attribute').all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#
# class AttributeValueDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = AttributeValueSerializer
#     queryset = AttributeValue.objects.all()


# class AttributeValueList(APIView):
#     def get(self, request):
#         attribute_value_queryset = AttributeValue.objects.select_related('product', ' attribute').all()
#         serializer = AttributeValueSerializer(attribute_value_queryset, many=True)
#         return Response(serializer.data)
#     def post(self, request):
#         serializer = AttributeValueSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('attribute value is posting')


# class AttributeValueDetail(APIView):
#     def get(self, request, pk):
#         attribute_value = get_object_or_404(AttributeValue, pk=pk)
#         serializer = AttributeValueSerializer(attribute_value)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         attribute_value = get_object_or_404(AttributeValue, pk=pk)
#         serializer = AttributeValueSerializer(attribute_value, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         attribute_value = get_object_or_404(AttributeValue, pk=pk)
#         attribute_value.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def attribute_value_list(request):
#     if request.method == 'GET':
#         attribute_value_queryset = AttributeValue.objects.select_related('product', ' attribute').all()
#         serializer = AttributeValueSerializer(attribute_value_queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = AttributeValueSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('attribute value is posting')


# @api_view(['GET', 'PUT', 'DELETE'])
# def attribute_value_detail(request, pk):
#     attribute_value = get_object_or_404(AttributeValue, pk=pk)
#     if request.method == 'GET':
#         serializer = AttributeValueSerializer(attribute_value)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = AttributeValueSerializer(attribute_value, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         attribute_value.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# class VariantList(ListCreateAPIView):
#     serializer_class = VariantSerializer
#     queryset = Variant.objects.select_related('product', 'color', 'size').all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#
# class VariantDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = VariantSerializer
#     queryset = Variant.objects.all()


# class VariantList(APIView):
#     def get(self, request):
#         variant_queryset = Variant.objects.select_related('product', 'color', 'size').all()
#         serializer = VariantSerializer(variant_queryset, many=True)
#         return Response(serializer.data)
#     def post(self, request):
#         serializer = VariantSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('variant list is posting')

# class VariantDetail(APIView):
#     def get(self, request, pk):
#         variant = get_object_or_404(Variant, pk=pk)
#         serializer = VariantSerializer(variant)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         variant = get_object_or_404(Variant, pk=pk)
#         serializer = VariantSerializer(variant, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         variant = get_object_or_404(Variant, pk=pk)
#         variant.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def variant_list(request):
#     if request.method == 'GET':
#         variant_queryset = Variant.objects.select_related('product', 'color', 'size').all()
#         serializer = VariantSerializer(variant_queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = VariantSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('variant list is posting')


# @api_view(['GET', 'PUT', 'DELETE'])
# def variant_detail(request, pk):
#     variant = get_object_or_404(Variant, pk=pk)
#     if request.method == 'GET':
#         serializer = VariantSerializer(variant)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = VariantSerializer(variant, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         variant.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# class ImageList(ListCreateAPIView):
#     serializer_class = ImageSerializer
#     queryset = Image.objects.select_related('product').all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#
# class ImageDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = ImageSerializer
#     queryset = Image.objects.all()


# class ImageList(APIView):
#     def get(self, request):
#         image_queryset = Image.objects.select_related('product').all()
#         serializer = ImageSerializer(image_queryset, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = ImageSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('image list is posting')


# class ImageDetail(APIView):
#     def get(self, request, pk):
#         image = get_object_or_404(Image, pk=pk)
#         serializer = ImageSerializer(image)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         image = get_object_or_404(Image, pk=pk)
#         serializer = ImageSerializer(image, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         image = get_object_or_404(Image, pk=pk)
#         image.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def image_list(request):
#     if request.method == 'GET':
#         image_queryset = Image.objects.select_related('product').all()
#         serializer = ImageSerializer(image_queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ImageSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('image list is posting')


# @api_view(['GET', 'PUT', 'DELETE'])
# def image_detail(request, pk):
#     image = get_object_or_404(Image, pk=pk)
#     if request.method == 'GET':
#         serializer = ImageSerializer(image)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ImageSerializer(image, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         image.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# class ProductCommentList(ListCreateAPIView):
#     serializer_class = ProductCommentSerializer
#     queryset = ProductComment.objects.select_related('product', 'user').all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#
# class ProductCommentDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = ProductCommentSerializer
#     queryset = ProductComment.objects.all()


# class ProductCommentList(APIView):
#     def get(self, request):
#         comment_queryset = ProductComment.objects.select_related('product', 'user').all()
#         serializer = ProductCommentSerializer(comment_queryset, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = ProductCommentSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('product comment list is posting.')


# class ProductCommentDetail(APIView):
#     def get(self, request, pk):
#         product_comment = get_object_or_404(ProductComment, pk=pk)
#         serializer = ProductCommentSerializer(product_comment)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         product_comment = get_object_or_404(ProductComment, pk=pk)
#         serializer = ProductCommentSerializer(product_comment, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         product_comment = get_object_or_404(ProductComment, pk=pk)
#         product_comment.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def product_comment_list(request):
#     if request.method == 'GET':
#         comment_queryset = ProductComment.objects.select_related('product', 'user').all()
#         serializer = ProductCommentSerializer(comment_queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductCommentSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('product comment list is posting.')


# @api_view(['GET', 'PUT', 'DELETE'])
# def product_comment_detail(request, pk):
#     product_comment = get_object_or_404(ProductComment, pk=pk)
#     if request.method == 'GET':
#         serializer = ProductCommentSerializer(product_comment)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductCommentSerializer(product_comment, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         product_comment.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# class OrderList(ListCreateAPIView):
#     serializer_class = OrderSerializer
#     queryset = Order.objects.select_related('customer').all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#
# class OrderDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = OrderSerializer
#     queryset = Order.objects.all()


# class OrderList(APIView):
#     def get(self, request):
#         order_queryset = Order.objects.select_related('customer').all()
#         serializer = OrderSerializer(order_queryset, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = OrderSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('order list is posting')


# class OrderDetail(APIView):
#     def get(self, request, pk):
#         order = get_object_or_404(Order, pk=pk)
#         serializer = OrderSerializer(order)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         order = get_object_or_404(Order, pk=pk)
#         serializer = OrderSerializer(order, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         order = get_object_or_404(Order, pk=pk)
#         order.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def order_list(request):
#     if request.method == 'GET':
#         order_queryset = Order.objects.select_related('customer').all()
#         serializer = OrderSerializer(order_queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = OrderSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('order list is posting')


# @api_view(['GET', 'PUT', 'DELETE'])
# def order_detail(request, pk):
#     order = get_object_or_404(Order, pk=pk)
#     if request.method == 'GET':
#         serializer = OrderSerializer(order)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = OrderSerializer(order, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         order.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class OrderItemList(ListCreateAPIView):
#     serializer_class = OrderItemSerializer
#     queryset = OrderItem.objects.select_related('order', 'product').all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#
# class OrderItemDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = OrderItemSerializer
#     queryset = Order.objects.all()


# class OrderItemList(APIView):
#     def get(self, request):
#         order_item_queryset = OrderItem.objects.select_related('order', 'product').all()
#         serializer = OrderItemSerializer(order_item_queryset, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = OrderItemSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

# class OrderItemDetail(APIView):
#     def get(self, request, pk):
#         order_item = get_object_or_404(OrderItem, pk=pk)
#         serializer = OrderItemSerializer(order_item)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         order_item = get_object_or_404(OrderItem, pk=pk)
#         serializer = OrderItemSerializer(order_item, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         order_item = get_object_or_404(OrderItem, pk=pk)
#         order_item.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def order_item_list(request):
#     if request.method == 'GET':
#         order_item_queryset = OrderItem.objects.select_related('order', 'product').all()
#         serializer = OrderItemSerializer(order_item_queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = OrderItemSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# @api_view(['GET', 'PUT', 'DELETE'])
# def order_item_detail(request, pk):
#     order_item = get_object_or_404(OrderItem, pk=pk)
#     if request.method == 'GET':
#         serializer = OrderItemSerializer(order_item)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = OrderItemSerializer(order_item, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         order_item.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class CartList(ListCreateAPIView):
#     serializer_class = CartSerializer
#     queryset = Cart.objects.all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#
# class CartDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = CartSerializer
#     queryset = Cart.objects.all()


# class CartList(APIView):
#     def get(self, request):
#         cart_queryset = Cart.objects.all()
#         serializer = CartSerializer(cart_queryset, many=True)
#         return Response(serializer.data)
#
#     def post(self,request):
#         serializer = CartSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('cart list is posting')


# class CartDetail(APIView):
#     def get(self, request, pk):
#         cart = get_object_or_404(Cart, pk=pk)
#         serializer = CartSerializer(cart)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         cart = get_object_or_404(Cart, pk=pk)
#         serializer = CartSerializer(cart, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         cart = get_object_or_404(Cart, pk=pk)
#         cart.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def cart_list(request):
#     if request.method == 'GET':
#         cart_queryset = Cart.objects.all()
#         serializer = CartSerializer(cart_queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CartSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('cart list is posting')


# @api_view(['GET', 'PUT', 'DELETE'])
# def cart_detail(request, pk):
#     cart = get_object_or_404(Cart, pk=pk)
#     if request.method == 'GET':
#         serializer = CartSerializer(cart)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CartSerializer(cart, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         cart.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class CartItemList(ListCreateAPIView):
#     serializer_class = CartItemSerializer
#     queryset = CartItem.objects.select_related('cart', 'product').all()
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#
# class CartItemDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = CartItemSerializer
#     queryset = CartItem.objects.all()

# class CartItemList(APIView):
#     def get(self, request):
#         cart_item_queryset = CartItem.objects.select_related('cart', 'product').all()
#         serializer = CartItemSerializer(cart_item_queryset, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         cart_item_queryset = CartItem.objects.select_related('cart', 'product').all()
#         serializer = CartItemSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# class CartItemDetail(APIView):
#     def get(self, request, pk):
#         cart_item = get_object_or_404(CartItem, pk=pk)
#         serializer = CartItemSerializer(cart_item)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         cart_item = get_object_or_404(CartItem, pk=pk)
#         serializer = CartItemSerializer(cart_item, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         cart_item = get_object_or_404(CartItem, pk=pk)
#         cart_item.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def cart_item_list(request):
#     cart_item_queryset = CartItem.objects.select_related('cart', 'product').all()
#     if request.method == 'GET':
#         serializer = CartItemSerializer(cart_item_queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CartItemSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

# @api_view(['GET', 'PUT', 'DELETE'])
# def cart_item_detail(request, pk):
#     cart_item = get_object_or_404(CartItem, pk=pk)
#     if request.method == 'GET':
#         serializer = CartItemSerializer(cart_item)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CartItemSerializer(cart_item, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         cart_item.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
