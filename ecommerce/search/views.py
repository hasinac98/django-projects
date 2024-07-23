from django.shortcuts import render
from shop.models import Product


def search_products(request):
    p=None
    query = ""
    if request.method=='POST':
        query=request.POST['q']
        if query:
            p=Product.objects.filter(name__icontains=query)
    return render(request,'searchproduct.html',{'p':p,'query':query})