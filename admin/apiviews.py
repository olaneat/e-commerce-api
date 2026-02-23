from orders.models import Order, Item, OrderItem
from products.models import ProductModel, CategoryModel
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from orders.serializers import OrderSerializer, ItemSerializer, OrderListSerializer, VerifyPaymentSeializer
from django.db.models import Count



class StatusCountAPI(APIView):
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

    def get(self, request):
        pending_payment_count = Order.objects.filter(status='pending_payment').count()
        processing_count = Order.objects.filter(status='processing').count()
        intransit_count = Order.objects.filter(status='intransit').count()
        delivered_count = Order.objects.filter(status='delivered').count()


        data = {
            'pending_payment': pending_payment_count,
            'intransit_count': intransit_count,
            'delivered_count': delivered_count,
            'processing_count': processing_count

        }
        return Response({'data':data, 'msg': 'status count fetched successfully', 'status_code': 200})


class DisplayOrders(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    serializer_class = OrderListSerializer
    queryset = Order.objects.all()