# orders/filters.py
from django_filters import rest_framework as filters
from .models import Order

class OrderFilter(filters.FilterSet):
    status = filters.ChoiceFilter(
        label="Status",
        empty_label="All Status"
    )
    reference = filters.CharFilter(lookup_expr='icontains', label="Reference")
    # payment_status = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = Order
        fields = ['status', 'reference', 'payment_status']