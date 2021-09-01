from django.http.response import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .forms import OrderCreateForm
from .models import Order, OrderItem
from cart.cart import Cart
from .tasks import order_created
from django.conf import settings
from django.template.loader import render_to_string
import weasyprint

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'], 
                                        price=item['price'], 
                                        quantity=item['quantity'])
            #  clear the cart
            cart.clear()
            # Launch asynchronous task with celery
            order_created.delay(order.id)
            # Set the order to the session
            request.session['order_id'] = order.id
            # redirect for payment
            template_name = 'orders/order/created.html'
            context = {
                'order': order
            }
            return redirect(reverse('payment:process'))            
    else:
        form = OrderCreateForm()
    
    template_name = 'orders/order/create.html'
    context = {
        'cart': cart,
        'form': form
    }

    return render(request, template_name, context)
    

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    template_name = 'admin/orders/order/detail.html'
    context = {
        'order': order
    }

    return render(request, template_name, context)


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f"filename=oder_{order.id}.pdf"
    weasyprint.HTML(string=html).write_pdf(response,
            stylesheets=[weasyprint.CSS(
                str(settings.STATIC_ROOT) + '/css/pdf.css'
            )])
    return response