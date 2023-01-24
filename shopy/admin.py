from django.contrib import admin
from shopy.models import Product, Reserved, Account, User


admin.site.register(Product)

admin.site.register(Reserved)

admin.site.register(Account)

admin.site.register(User)
