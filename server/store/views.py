# from django.http import JsonResponse
# # Create your views here.
# def home(request):
#     data={"message":"API working"}
#     return JsonResponse(data)

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes   
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.models import User
from .models import ProductModel,CategoryModel,CartModel,CartItemModels,OrderModel,OrderItemModels
from .serializers import CartItemSerializer,ProductSerializer,CategorySerializer,CartSerializer,UserSerializer,RegisteredSerializer
from rest_framework import status
@api_view(['GET'])
def get_products(request):
    products=ProductModel.objects.all()
    serializer=ProductSerializer(products,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_product(request,pk):
     try:
        product=ProductModel.objects.get(id=pk)
        serializer=ProductSerializer(product,context={'request':request})
        return Response(serializer.data)
     except ProductModel.DoesNotExist:
         return Response({'error':'product not found'},status=404)
        





@api_view(['GET'])
def get_categery(request):
    category=CategoryModel.objects.all()
    serializer=CategorySerializer(category,many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart,created=CartModel.objects.get_or_create(users=request.user)
    serializer=CartSerializer(cart)
    return Response(serializer.data)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id=request.data.get('product_id')
    product=ProductModel.objects.get(id=product_id)
    cart,created=CartModel.objects.get_or_create(users=request.user)
    item,created=CartItemModels.objects.get_or_create(cart=cart,product=product)
    if not created:
        item.quantity+=1
        item.save() 
    return Response({'message':"Product added to cart","cart":CartSerializer(cart).data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    item_id=request.data.get('item_id')
    CartItemModels.objects.filter(id=item_id).delete()
    return Response({"message":"Item removed from cart"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_to_cart(request):
    item_id=request.data.get('item_id')
    quantity=request.data.get('quantity')
    
    if not item_id or quantity is None:
        return Response({'error':"Item ID and quantity is required "},status=400)
    try:
        item = CartItemModels.objects.get(id=item_id)
        if int(quantity)<1:
            return Response({'error':'Qauantity must be atleast 1'},status=400)
        item.quantity=quantity
        item.save()
        serializer=CartItemSerializer(item)
        return Response(serializer.data)
    except CartItemModels.DoesNotExist:
        return Response({'error':'Cart cant be found '},status=404)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_order(request):
    try:
        data = request.data

        name = data.get('name')
        address = data.get('address')
        phone = data.get('phone')
        payment_method = data.get('payment_method', 'cod')
        #valid phone 
        if not phone.isdigit() or len(phone) < 10:
            return Response({'error': "Invalid phone number"}, status=400)
        
        cart = CartModel.objects.filter(user=request.user).first()


        if not cart or not cart.items.exists():
            return Response({'error': "Cart is empty"}, status=400)

        total = sum(
         [   float(item.product.price) * item.quantity
            for item in cart.items.all()]
        )
#create order
        order = OrderModel.objects.create(
            user=request.user,
            total_amount=total
        )
#create Order items create
        for item in cart.items.all():
            OrderItemModels.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart.items.all().delete()

        return Response({
            'message': "Order placed successfully",
            'order_id': order.id
        })

    except Exception as e:
        return Response({'error': str(e)}, status=500)

 
 
 

@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    serializer=RegisteredSerializer(data=request.data)
    if serializer.is_valid():
        user=serializer.save()
        user_serializer=UserSerializer(user)
        return Response({'message':'User registered successfully',"user":user_serializer.data},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


 