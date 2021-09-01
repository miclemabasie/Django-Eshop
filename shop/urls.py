from django.urls import path
from django.urls.conf import include
from .views import (
    product_list_view,
    product_detail_view
)

app_name = 'products'


urlpatterns = [
    path('', product_list_view, name='product_list'), 
    path('category/<slug:category_slug>/', product_list_view, name='category_product_list'), 
    path('prducts/<int:id>/<slug:slug>/', product_detail_view, name='product_detail')
]
