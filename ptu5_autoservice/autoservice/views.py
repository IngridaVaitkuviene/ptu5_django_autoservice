from django.shortcuts import render
from django.http import HttpResponse
from . models import Car, Service, Order

# Create your views here.
def index(request):
    # return HttpResponse("Hello, the autoservice is at Your services!")
    service_count = Service.objects.count()
    order_count = Order.objects.count()
    car_count = Car.objects.count()

    context = {
        'service_count' : service_count,
        'order_count' : order_count,
        'car_count' : car_count
    }

    return render(request, 'autoservice/index.html', context)