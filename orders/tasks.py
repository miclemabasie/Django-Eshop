from celery import task
from django.core.mail import send_mail
from .models import Order
from django.shortcuts import get_object_or_404

@task
def order_created(order_id):
    """
        Task to send an e-mail notification when and order is successfully created.
    """

    order = get_object_or_404(Order, id=order_id)
    subject = f"Order nr. {order.id}"
    message = f"Dear {order.first_name}, \n\n" \
              f"You have successfully placed an order." \
              f"You order ID is {order.id}."
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])

    return mail_sent