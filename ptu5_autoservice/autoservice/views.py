from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from . models import Car, Service, Order
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def index(request):
    # return HttpResponse("Hello, the autoservice is at Your services!")
    service_count = Service.objects.count()
    order_count = Order.objects.count()
    car_count = Car.objects.count()
    visits_count = request.session.get('visits_count', 1)
    request.session['visits_count'] = visits_count + 1

    context = {
        'service_count' : service_count,
        'order_count' : order_count,
        'car_count' : car_count,
        'visits_count': visits_count,
    }

    return render(request, 'autoservice/index.html', context)

def cars(request):
    paginator = Paginator(Car.objects.all(), 3)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    return render(request, 'autoservice/cars.html', {'cars': paged_cars})

def car_info(request, car_id):
    return render(request, 'autoservice/car_info.html', {'car': get_object_or_404(Car, id=car_id)})

class OrderlistView(ListView):
    model = Order
    paginate_by = 3
    template_name = 'autoservice/order_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(car__owner__icontains=search) | 
                Q(car__plate_number__icontains=search) | 
                Q(car__VIN_code__icontains=search)
                # Q(car_model___model__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders_count'] = self.get_queryset().count()
        return context

    
class OrderDetailView(DetailView):
    model = Order
    template_name = 'autoservice/order_detail.html'


class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'autoservice/user_order_list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(reader=self.request.user)
        return queryset