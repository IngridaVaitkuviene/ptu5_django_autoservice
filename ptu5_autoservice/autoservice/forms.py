from django import forms
from . models import OrderReview, Order
from django.utils.timezone import datetime, timedelta


class OrderReviewForm(forms.ModelForm):
    def is_valid(self):
        valid = super().is_valid()
        if valid:
            owner = self.cleaned_data.get("owner")
            recent_posts = OrderReview.objects.filter(owner=owner, created_at__gte=(datetime.now() - timedelta(minutes=1)))
            if recent_posts:
                return False
        return valid
    class Meta:
        model = OrderReview
        fields = ('content', 'order', 'owner')
        widgets = {
            'order': forms.HiddenInput(),
            'owner': forms.HiddenInput(),
        }


class DateInput(forms.DateInput):
    input_type = 'date'


class UserOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('car', 'estimate_date',)
        widgets = {'estimate_date': DateInput()}


class UserOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('car', 'estimate_date',)
        widgets = {'estimate_date': DateInput(), 'car': forms.HiddenInput()}