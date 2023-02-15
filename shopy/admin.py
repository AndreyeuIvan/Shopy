from django.contrib import admin
from shopy.models import Reserved


@admin.register(Reserved)
class ReservedtAdmin(admin.ModelAdmin):
    readonly_fields = ("total_price",)
    list_display = ("product",)
