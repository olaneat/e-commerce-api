from django.urls import path
from  .apiviews import StatusCountAPI, DisplayOrders


app_name = 'admin-section'
urlpatterns = [    
    path('status-count', StatusCountAPI.as_view(), name='status-count'),
    path('order-list', DisplayOrders.as_view(), name='display-orders'),
]