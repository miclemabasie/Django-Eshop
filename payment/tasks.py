from io import BytesIO
from celery import task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@task
def payment_completed(order_id):
    """
    Task to send and e-mail notification when an order id successfully created.
    """
    order = Order.objects.get(id=order_id)

    # create invoice e-mail
    subject = f"My Shop - EE Invoice no. {order.id}"
    message = "Please, find attached the invoice for your recent purchase"
    email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])

    # Generate the PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(str(settings.STATIC_ROOT) + '/css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # attacht e-mail
    email.attach(f"order_{order.id}.pdf",
                    out.getvalue(),
                    'application/pdf')

    # Send the e-mail
    print('sending email')
    email.send()
