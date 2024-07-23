from django.shortcuts import render,redirect
from shop.models import Category,Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

def home(request):
    return render(request,'base.html')

def category(request):
    item = Category.objects.all()
    return render(request,'category.html',{'item':item})

def product(request,i):
    c= Category.objects.get(id=i)
    p= Product.objects.filter(category=c)
    return render(request, 'product.html', {'c':c,'p':p})

def productdetails(request,i):
    t=Product.objects.get(id=i)
    return render(request,'productdetails.html',{'t':t})

def register(request):
    if (request.method == "POST"):  # after submission
        u = request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        fn = request.POST['fn']
        ln = request.POST['ln']
        e = request.POST['e']
        if(cp==p):
            user = User.objects.create_user(username=u, password=p, first_name=fn, last_name=ln, email=e)
            user.save()
            return redirect('shop:home')
    return render(request, 'register.html')

def user_login(request):
    u = request.POST.get('u')
    p = request.POST.get('p')
    user = authenticate(username=u,password=p)
    if user:
        login(request,user)
        return redirect('shop:home')
    else:
        messages.error(request,'invalid credentials')

    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('shop:user_login')
