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
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

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

#

class RevenueAnalyticsView(APIView):
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    def get(self, request):
        period = request.query_params.get('period', 'days').lower()
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')

        queryset = Order.objects.all()

        # End date = today
        end = timezone.now().date()

        if period == 'custom':
            if not (start_date and end_date):
                return Response({"error": "start and end dates required for custom period"}, status=400)
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__date__range=[start, end])
            except ValueError:
                return Response({"error": "Invalid date format"}, status=400)
            trunc_kind = TruncDay('created_at')  # Fallback; customize if needed
            date_format = '%Y-%m-%d'  # Full date for custom
        else:
            if period == 'days':
                start = end - timedelta(days=6)  # Last 7 days
                trunc_kind = TruncDay('created_at')
                date_format = '%a'  # Mon, Tue, etc.
            elif period == 'weeks':
                start = end - timedelta(weeks=12)
                trunc_kind = TruncWeek('created_at')
                date_format = '%Y-%m-%d'  # Week start date
            elif period == 'months':
                start = end + relativedelta(months=-12)
                trunc_kind = TruncMonth('created_at')
                date_format = '%Y-%m'
            elif period == 'years':
                start = end.replace(month=1, day=1) - relativedelta(years=5)
                trunc_kind = TruncYear('created_at')
                date_format = '%Y'
            else:
                return Response({"error": "Invalid period"}, status=400)

            queryset = queryset.filter(created_at__date__range=[start, end])

        # Aggregate by period (normalize keys to date)
        aggregated = (
            queryset
            .annotate(period=trunc_kind)
            .values('period')
            .annotate(total=Sum('total_amount'))
            .order_by('period')
        )
        agg_dict = {item['period'].date(): float(item['total'] or 0) for item in aggregated}  # Normalize to date

        # Generate full range with zeros
        data = []
        current = start
        while current <= end:
            if period == 'days' or period == 'custom':
                key = current
                increment = timedelta(days=1)
            elif period == 'weeks':
                key = current - timedelta(days=current.weekday())  # Monday (week start)
                increment = timedelta(weeks=1)
            elif period == 'months':
                key = current.replace(day=1)
                increment = relativedelta(months=1)
            elif period == 'years':
                key = current.replace(month=1, day=1)
                increment = relativedelta(years=1)

            revenue = agg_dict.get(key, 0.0)
            label = key.strftime(date_format)

            data.append({
                "date": label,
                "revenue": revenue,
            })

            current += increment  # Increment after adding

        # Overall total
        overall_total = sum(item['revenue'] for item in data)
        return Response({
            "overall_total": overall_total,
            "data": data[::-1],  # Reverse to newest first (today back)
            "period": period,
        })