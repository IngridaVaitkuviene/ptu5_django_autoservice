from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.contrib.auth import get_user_model
from django.utils.timezone import datetime
from tinymce.models import HTMLField

class CarModel(models.Model):
    YEARS_CHOICES = ((years, str(years)) for years in reversed(range(1900, date.today().year+1)))

    year = models.IntegerField(_("year"), choices=YEARS_CHOICES)
    make = models.CharField(_("make"), max_length=50)
    model = models.CharField(_("model"), max_length=50)
    engine = models.CharField(_("engine"), max_length=50)
    

    class Meta:
        verbose_name = 'Car model'
        verbose_name_plural = 'Car models'

    def __str__(self) -> str:
        return f'{self.make}, {self.model}, {self.engine}, {self.year}'


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
    cover = models.ImageField(_("cover"), upload_to='covers', blank=True, null=True)
    description = HTMLField(_("description"), max_length=1000, default='---')
    
    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'

    def __str__(self) -> str:
        return f'{self.car_model.make}, {self.car_model.model}, {self.plate_number}, {self.owner}'


class Service(models.Model):
    name = models.CharField(_("service name"), max_length=50)
    price = models.DecimalField(_("service price"), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self) -> str:
        return f'{self.name}- {self.price}'


class Order(models.Model):
    STATUS_CHOICES = (
        ('n', _('new')),
        ('a', _('advance payment taken')),
        ('o', _('ordered parts')),
        ('w', _('working')),
        ('d', _('done')),
        ('c', _('cancelled')),
        ('p', _('paid')),
    )
    car = models.ForeignKey(
        Car, 
        verbose_name=_("car"), 
        on_delete=models.CASCADE,
        related_name='orders'
    )
    date = models.DateField(_("order date"), auto_now_add=True, editable=False)
    total_sum = models.DecimalField(_("total amount"), max_digits=10, decimal_places=2, default=0)
    status = models.CharField(_("status"), max_length=1, choices=STATUS_CHOICES, default='n')
    estimate_date = models.DateField(_("estimate date"), null=True, blank=True)
    reader = models.ForeignKey(
        get_user_model(),
        verbose_name='reader',
        on_delete=models.SET_NULL,
        null=True, blank=True,
    )

    @property
    def is_overdue(self):
        if self.estimate_date and self.estimate_date < datetime.date(datetime.now()):
            return True
        return False

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def get_total(self):
        total = 0
        for line in self.order_lines.all():
            total += line.total_sum
        return total

    def save(self, *args, **kwargs):
        if not self._state.adding:
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
    quantity = models.IntegerField(_("quantity"), default=1)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Order line'
        verbose_name_plural = 'Order lines'

    @property
    def total_sum(self):
        return self.quantity * self.price

    def __str__(self) -> str:
        return f'{self.service.name}: {self.quantity} x {self.price}'


class OrderReview(models.Model):
    order = models.ForeignKey(
        Order, verbose_name="order", 
        on_delete=models.CASCADE, 
        related_name='reviews',
    )
    owner = models.ForeignKey(
        get_user_model(), 
        verbose_name="owner", 
        on_delete=models.CASCADE, 
        related_name='order_reviews',
    )
    created_at = models.DateTimeField("created at", auto_now_add=True)
    content = models.TextField("content", max_length=10000)

    def __str__(self) -> str:
        return f"{self.owner} on {self.order} at {self.created_at}"

    class Meta:
        ordering = ('-created_at', )