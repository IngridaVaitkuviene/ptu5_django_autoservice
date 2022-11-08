from django.db import models
from django.utils.translation import gettext_lazy as _

class CarModel(models.Model):
    YEARS_CHOICES = ((years, str(years)) for years in reversed(range(1900, 2023)))

    year = models.IntegerField(_("year"), choices=YEARS_CHOICES)
    make = models.CharField(_("make"), max_length=50)
    model = models.CharField(_("model"), max_length=50)
    engine = models.CharField(_("engine"), max_length=50)

    def __str__(self) -> str:
        return f'{self.year}, {self.make}, {self.model}, {self.engine}'

class Car(models.Model):
    car_model = models.ForeignKey(
        CarModel, 
        verbose_name=_("car model"), 
        on_delete=models.CASCADE, 
        related_name='cars'
    )
    plate_number = models.CharField(_("plate number"), max_length=50)
    VIN_code = models.CharField(_("VIN"), max_length=17, help_text='Vehicle identification number')
    owner = models.CharField(_("owner name"), max_length=100)

    def __str__(self) -> str:
        return f'{self.car_model.make}, {self.car_model.model}, {self.plate_number}, {self.owner}'

class Service(models.Model):
    name = models.CharField(_("service name"), max_length=50)
    price = models.DecimalField(_("service price"), max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name

class Order(models.Model):
    car = models.ForeignKey(
        Car, 
        verbose_name=_("car"), 
        on_delete=models.CASCADE,
        related_name='orders'
    )
    date = models.DateField(_("order date"), auto_now_add=True)
    total_sum = models.DecimalField(_("total amout"), max_digits=10, decimal_places=2, default=0)

    def get_total(self):
        total = 0
        for line in self.order_lines.all():
            total += line.total_sum
        return total

    def save(self, *args, **kwargs):
        self.total_sum = self.get_total()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.date}: {self.total_sum}, {self.car.plate_number} {self.car.owner}"

class OrderLine(models.Model):
    order = models.ForeignKey(
        Order, 
        verbose_name=_("order"), 
        on_delete=models.CASCADE,
        related_name='order_lines'
    )
    service = models.ForeignKey(
        Service, 
        verbose_name=_("service"), 
        on_delete=models.CASCADE,
        related_name='order_lines'
    )
    quantity = models.IntegerField(_("quantity"))
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)

    @property
    def total_sum(self):
        return self.quantity * self.price

    def __str__(self) -> str:
        return f'{self.service.name}: {self.quantity} x {self.price}'