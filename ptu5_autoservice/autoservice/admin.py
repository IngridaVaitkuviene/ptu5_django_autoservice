from django.contrib import admin
from . import models

class CarAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'VIN_code', 'owner')
    list_filter = ('car_model', 'owner')
    search_fields = ('VIN_code', 'plate_number')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

class OrderLineInLine(admin.TabularInline):
    model = models.OrderLine
    extra = 0
    can_delete = False

class OrderAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_sum', 'car', 'status', 'estimate_date', 'is_overdue', 'reader')
    inlines = (OrderLineInLine, )
    readonly_fields = ('date',)
    list_editable = ('estimate_date', 'reader')

    fieldsets = (
        ('Car', {'fields': ('car', 'total_sum', 'status', 'estimate_date')}),
        ('Date', {'fields': ('date',)})
    )

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('service', 'quantity', 'price', 'total_sum', 'order')
    ordering = ('order', 'id')
    list_filter = ('order', )

# Register your models here.
admin.site.register(models.Car, CarAdmin)
admin.site.register(models.CarModel)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderLine, OrderLineAdmin)