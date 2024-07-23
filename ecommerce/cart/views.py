from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from .models import Product
from .models import Cart
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import razorpay
from cart.models import Payment
from django.views.decorators.csrf import csrf_exempt
from .models import Order_table


@login_required
def add_to_cart(request,id):
    p=Product.objects.get(id=id)
    u=request.user

    try:
        cart=Cart.objects.get(user=u,product=p)
        if (p.stock > 0):
            cart.quantity += 1
            cart.save()
            p.stock -= 1
            p.save()
    except:
        if(p.stock):
            cart= Cart.objects.create(product=p,user=u,quantity=1)
            cart.save()
            p.stock -= 1
            p.save()
    return redirect('cart:cart_view')

def cart_view(request):
    u=request.user
    cart= Cart.objects.filter(user=u)

    total=0
    for i in cart:
        total+=total+i.quantity*i.product.price

    return render(request,'cart_view.html',{'cart':cart,'total':total})
@login_required
def cart_decrement(request,id):
    p = Product.objects.get(id=id)
    u = request.user
    try:
       cart = Cart.objects.get(user=u, product=p)
       if(cart.quantity>1):
           cart.quantity -=1
           cart.save()
           p.stock +=1
           p.save()
       else:
           cart.delete()
           p.stock +=1
           p.save()
    except:
        pass
    return redirect('cart:cart_view')

@login_required
def cart_delete(request,id):
    p = Product.objects.get(id=id)
    u = request.user
    try:
         cart = Cart.objects.get(user=u, product=p)
         cart.delete()
         p.stock +=cart.quantity
         p.save()
    except:
        pass
    return redirect('cart:cart_view')

def place_order(request):
    if(request.method=='POST'):
        ph=request.POST.get('phone')
        a=request.POST.get('address')
        n=request.POST.get('pin')
        u=request.user
        c=Cart.objects.filter(user=u)

        total=0
        for i in c:
            total=total+(i.quantity*i.product.price)
        total=int(total*100)

        client= razorpay.Client(auth=('rzp_test_uA5YAQ8zd15ZJS','MByBXTkvt6S3hQYOa3qdM2pn'))

        response_payment=client.order.create(dict(amount=total,currency='INR'))

        print(response_payment)
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status=="created":
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            p.save()

            for i in c:
                o = Order_table.objects.create(user=u, product=i.product, address=a, phone=ph, pin=n,
                                               no_of_items=i.quantity, order_id=order_id)

                o.save()
        response_payment['name']=u.username
        return render(request,'payment.html',{'payment':response_payment})
    return render(request, 'order_form.html')

@csrf_exempt
def payment_status(request,u):
    print(request.user.is_authenticated)  #false
    if not request.user.is_authenticated:
        user = User.objects.get(username=u)
        login(request,user)
        print(request.user.is_authenticated) #true

    if(request.method=="POST"):
        response = request.POST
        # print(response)
        # print(u)
        # print(response)
        param_dict = {
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_signature': response['razorpay_signature']
        }
        client = razorpay.Client(auth=('rzp_test_uA5YAQ8zd15ZJS', 'MByBXTkvt6S3hQYOa3qdM2pn'))

        try:
            status=client.utility.verify_payment_signature(param_dict)
            print(status)
            ord = Payment.objects.get(order_id=response['razorpay_order_id'])
            ord.razorpay_payment_id = response['razorpay_payment_id']
            ord.paid = True
            ord.save()

            u=User.objects.get(username=u)
            c=Cart.objects.filter(user=u)

            o=Order_table.objects.filter(user=u,order_id=response['razorpay_order_id'])
            for i in o:
                i.payment_status= "paid"
                i.save()
            c.delete()
            return render(request,'payment_status.html',{'status':True})
        except:

            return render(request,'payment_status.html',{'status':False})

@login_required
def order_view(request):
    u=request.user

    customer = Order_table.objects.filter(user=u,payment_status="paid")

    return render(request,'order_view.html',{'customer':customer,'u':u.username})
