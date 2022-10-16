from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Car, Order,User

# Register your models here.
admin.site.register(Car)
admin.site.register(Order)
admin.site.register(User,UserAdmin)
