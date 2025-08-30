from django.urls import path
from .apiviews import CreateOrderAPIView
app_name = "orders"
urlpatterns = [
    path('create', CreateOrderAPIView.as_view(), name='order-create'),
    # path('list/', OrderListView.as_view(), name='order-list'),
    # path('detail/<uuid:pk>/', OrderDetailView.as_view(), name='order-detail'),
    # path('update/<uuid:pk>/', OrderUpdateView.as_view(), name='order-update'),
    # path('delete/<uuid:pk>/', OrderDeleteView.as_view(), name='order-delete'),
]
