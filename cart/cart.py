from decimal import Decimal
from shop.models import Product
from django.conf import settings
from coupons.models import Coupon


class Cart(object):

    def __init__(self, request):
        """
            Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the current session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store the current applied coupon
        self.coupon_id = self.session.get('coupon_id')


    def add(self, product, quantity=1, overwrite_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        
        if overwrite_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the current session.
        """

        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
        
    def __iter__(self):
        """
        Iterate over the  items in the cart and get the products from the database
        """

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart
        """

        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        # Return the total price of all the items in the cart
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # Remove cart form session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                print('######### No cart was found ##########')
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                print('############# no coupon found ############3')
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()