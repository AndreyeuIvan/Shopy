from django.contrib import admin
from shopy.models import Product, Reserved, Account, Shop


@admin.register(Reserved)
class ReservedtAdmin(admin.ModelAdmin):
    readonly_fields = ("total_price",)
    list_display = ("product",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("price_for_kilo",)


admin.site.register(Account)
admin.site.register(Shop)
