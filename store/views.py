from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json

# Create your views here.
def store(request):

    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            order = Order.objects.get(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items

        except Exception as e:
            #print(f'\n\n{request.user}  Vai Somosya Hoise {e}')
            items = [] 

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart']

    products = Product.objects.all()
    context = {'products':products}
    return render(request,  'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            order = Order.objects.get(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items

            #print(f'\n\n\Congratulations Total Items Found {items.count()} order {order.id} ')
        except Exception as e:
            #print(f'\n\n{request.user}  Vai Somosya Hoise {e}')
            items = []  

    # items = OrderItem.objects.all()
    # print(items , "******************************")
    # context = {'items':items}
    # return render(request, 'store/cart.html', context)

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    
    #context = {'items':items}
    #print(f'\n\nTotal Items Found {items}')
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            order = Order.objects.get(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items

        except Exception as e:
            #print(f'\n\n{request.user}  Vai Somosya Hoise {e}')
            items = [] 

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0} 
        cartItems = order.get_cart_items

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order = Order.objects.get(customer=customer, complete=False)
    OrderItem = OrderItem.objects.get(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)