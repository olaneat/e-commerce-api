from django.urls import path
from  .apiviews import StatusCountAPI, DisplayOrders, RevenueAnalyticsView


app_name = 'admin-section'
urlpatterns = [    
    path('status-count', StatusCountAPI.as_view(), name='status-count'),
    path('order-list', DisplayOrders.as_view(), name='display-orders'),
    path('revenue-metrics/', RevenueAnalyticsView.as_view(), name='revenue-metrics'),
]