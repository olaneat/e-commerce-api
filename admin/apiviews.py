from orders.models import Order, Item, OrderItem
from products.models import ProductModel, CategoryModel
from rest_framework import generics, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from orders.serializers import OrderSerializer, ItemSerializer, OrderListSerializer, VerifyPaymentSeializer
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import  RevenueAnalyticsSerializer, RevenueDataPointSerializer
from rest_framework import status
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncYear
from django.utils import timezone
from datetime import timedelta

from orders.orderFilter import OrderFilter

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

    def get_queryset(self):
        # user = self.request.user
        # queryset = Order.objects.all()
        orders = Order.objects.all()
        # orders = Order.objects.filter.order_by('-created_at')
        return orders
    # user = self.request.user
    #     print("CURRENT USER:", user.id, user.email)  # ← DEBUG LINE
    #     orders = Order.objects.filter(user=user).order_by('-created_at')
    #     print("ORDERS FOUND FOR USER:", orders.count(), [o.id for o in orders])
    #     return orders
    
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = OrderFilter
    
    search_fields = ['reference']

class RevenueAnalyticsView(APIView):
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

    def get(self, request):
        # Get the period parameter (e.g., 'daily', 'weekly', 'monthly')
        period = request.query_params.get('period', 'months').lower()
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')

        queryset = Order.objects.all()

        # Calculate revenue data based on the specified period
        if period == 'custom':
            if not (start_date and end_date):
                return Response(
                    {"error": "start and end dates required for custom period"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                start = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
                end = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__date__range=[start, end])
            except ValueError:
                return Response({"error": "Invalid date format"}, status=400)
            trunc_kind = TruncDay('created_at')  # fallback for custom

        else:
            # Default: last 30 days / reasonable window
            end = timezone.now().date()
            if period == 'days':
                start = end - timedelta(days=30)
                trunc_kind = TruncDay('created_at')
            elif period == 'weeks':
                start = end - timedelta(weeks=12)  # ~3 months
                trunc_kind = TruncWeek('created_at')
            elif period == 'months':
                start = end.replace(day=1) - timedelta(days=365)  # ~1 year back
                trunc_kind = TruncMonth('created_at')
            elif period == 'years':
                start = end.replace(month=1, day=1) - timedelta(days=365*5)  # 5 years
                trunc_kind = TruncYear('created_at')
            else:
                return Response({"error": "Invalid period"}, status=400)

            queryset = queryset.filter(created_at__date__gte=start)

        aggregated = (queryset
            .annotate(period=trunc_kind)
            .values('period')
            .annotate(total=Sum('total_amount'))
            .order_by('period')
        )

        # Format response
        data = [
            {
                "date": item['period'].strftime('%Y-%m-%d'),  # or customize format
                "revenue": float(item['total'] or 0),
            }
            for item in aggregated
        ]

        # Optional: total overall
        overall_total = sum(item['revenue'] for item in data)

        return Response({
            "overall_total": overall_total,
            "data": data,
            "period": period,
        })