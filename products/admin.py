from django import forms
from django.contrib import admin
from products.models import Category, Product, ProductImage, Review, ProductType

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage

class ReviewInline(admin.TabularInline):
    model = Review

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display =('name', 'category', 'product_type', 'size', 'collection', 'price')
    list_filter = ('category', 'product_type')
    list_editable = ('price', 'collection', 'size')
    inlines = [
        ProductImageInline,
        ReviewInline
    ]