from django.contrib import admin
from . import models

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('service', 'quantity', 'price', 'total_sum', 'order')
    ordering = ('order', 'id')
    list_filter = ('order', )

# Register your models here.
admin.site.register(models.Car)
admin.site.register(models.CarModel)
admin.site.register(models.Service)
admin.site.register(models.Order)
admin.site.register(models.OrderLine, OrderLineAdmin)