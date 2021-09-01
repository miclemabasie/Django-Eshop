from django.http.response import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Category, Product
from cart.forms import CartAddProductForm
from cart.cart import Cart



# Listing all the products
def product_list_view(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart = Cart(request)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    
    for item in cart:
        print(item)

    template_name = 'products/products-list.html'
    context = {
        'products': products,
        'categories': categories,
        'category': category,
        
    }
    
    return render(request, template_name, context)


# Product detail view
def product_detail_view(request, id, slug):
    product = get_object_or_404(Product, slug=slug, id=id)
    form = CartAddProductForm()
    template_name = 'products/product-detail.html'
    context = {
        'product': product,
        'form': form
    }

    return render(request, template_name, context)
