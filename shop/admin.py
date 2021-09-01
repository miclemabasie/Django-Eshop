from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available', 'created', 'updated')
    list_filter = ('name', 'category')
    list_editable = ('available', 'price')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', )


