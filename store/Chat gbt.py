from rest_framework.response import Response

# در ویو
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
        serializer.is_valid(raise_exception=True)  # ابتدا فراخوانی is_valid()
        serializer.save(customer=customer)  # اضافه کردن فیلد مشتری به سفارش
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'PUT':
        address = get_object_or_404(Address, customer_id=customer.id)
        serializer = UpdateAddressSerializer(address, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)  # ابتدا فراخوانی is_valid()
        serializer.save(customer=customer)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        address = get_object_or_404(Address, customer_id=customer.id)
        address.delete()
        return Response('The address successfully delete it.')
