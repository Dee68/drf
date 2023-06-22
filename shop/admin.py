from django.contrib import admin
from shop.models import Product, Review


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'count_in_stock', 'category',
                    'updated_at', 'in_stock', 'image_tag']
    readonly_fields = ['image_tag']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['name', 'price']
    search_fields = ('category','name',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'review', 'created_at']
    list_filter = ['user', 'created_at']

admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
