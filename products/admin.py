from django.contrib import admin
from products.models import Product, Shop


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("price_for_kilo",)


admin.site.register(Shop)
