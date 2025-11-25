from rest_framework.response import Response
from rest_framework import permissions 
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework import generics, filters
from .serializers import OrderSerializer, ItemSerializer, OrderListSerializer, VerifyPaymentSeializer
from .models import Order, Item
from .orderFilter import OrderFilter
from decouple import config
import requests
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

# from .models import OrderReference


class InitiatePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        data = request.data.copy()
        items_data = data.pop('items', [])
        if not items_data:
            return Response({
                'success': False,
                'message': 'No items provided',
                'status_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)
        callback_url = data.get('callback_url')
        serializer = OrderSerializer(data={'items': items_data, 'status': 'pending_payment', 'callback_url': callback_url}, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            payment_intent =  f"pi_{order.id}"
            order.payment_intent_id = payment_intent
            order.save()
            payment_url = 'https://api.paystack.co/transaction/initialize'
            amount_in_kobo = int(order.total_amount * 100) 
            
            callback_url = serializer.validated_data.get('callback_url')
            payload = {
                'reference': order.reference,
                'email': request.user.email,
                'amount': amount_in_kobo,
                "callback_url": callback_url
            }
            headers = {
                'Authorization': f'Bearer {config("PAYSTACK_SK")}',
                'Content-Type': 'application/json'
            }
            try:
                payment_response = requests.post(
                    payment_url,
                    json=payload,
                    headers=headers
                )
                payment_response.raise_for_status()
                paystack_data = payment_response.json()
                if paystack_data.get('status'):
                    payment_url = paystack_data['data']['authorization_url']
                    order.status = 'pending_payment'
                    order.save()
                    return Response({
                        'success': True,
                        'message': 'Order created successfully. Please proceed to payment.',
                        'status_code': status.HTTP_201_CREATED,
                        'data': {
                            'order_id': str(order.id),
                            'reference': order.reference,
                            'items': serializer.data['items_output'],
                            'total_amount': str(order.total_amount),
                            'payment_url': payment_url
                        }
                    }, status=status.HTTP_201_CREATED)
                else:
                    raise Exception(paystack_data.get('message', 'Payment initialization failed'))
            except requests.exceptions.RequestException as e:
                order.status = 'pending_payment'
                order.save()
                return Response({
                    'success': False,
                    'message': 'Payment initiation failed, order saved for retry',
                    'status_code': status.HTTP_402_PAYMENT_REQUIRED,
                    'data': {
                        'order_id': str(order.id),
                        'reference': order.reference,
                        'payment_url': paystack_data.get('data', {}).get('authorization_url', callback_url),  # Fallback URL
                        'items': serializer.data['items_output'],
                        'total_amount': str(order.total_amount)
                    }
                }, status=status.HTTP_402_PAYMENT_REQUIRED)
        return Response({
            'success': False,
            'message': 'Validation error',
            'status_code': status.HTTP_400_BAD_REQUEST,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
class ListOrdersView(generics.ListAPIView):
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderListSerializer

    def get_queryset(self):
        user = self.request.user
        # queryset = Order.objects.all()
        orders = Order.objects.filter(user=user).order_by('-created_at')
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
    # filterset_fields = {
    #     'status': ['icontains'],           # ← Works for ?status=pending
    #     'reference': ['exact', 'icontains'],
    #     # add more if you want
    # }
    search_fields = ['reference']
class DeleteOrderView(generics.DestroyAPIView):
    # lookup_field = 'id'
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()



# orders/apiviews.py
class PaymentCallbackView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        reference = request.query_params.get('reference')
        trxref = request.query_params.get('trxref')  # Paystack transaction reference
        if not reference:
            return Response({'error': 'No reference provided'}, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.filter(reference=reference).first()
        if not order:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        # Verify transaction with Paystack
        verify_url = f"https://api.paystack.co/transaction/verify/{trxref}"
        verify_headers = {
            'Authorization': f'Bearer {config("PAYSTACK_SECRET_KEY")}'
        }
        verify_response = requests.get(verify_url, headers=verify_headers)
        verify_data = verify_response.json()

        if verify_data.get('status') and verify_data['data']['status'] == 'success':
            order.status = 'processing'
            order.save()
            return Response({
                'success': True,
                'message': 'Payment successful',
                'order_id': str(order.id)
            }, status=status.HTTP_200_OK)
        else:
            order.status = 'pending_payment'
            order.save()
            return Response({
                'success': False,
                'message': 'Payment verification failed',
                'order_id': str(order.id),
                'payment_url': f"https://checkout.paystack.com/{order.payment_intent_id}"
            }, status=status.HTTP_402_PAYMENT_REQUIRED)
        
class VerifyPaymentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class=VerifyPaymentSeializer

    def get(self, request, reference):
        url = f'https://api.paystack.co/transaction/verify/{reference}'
        headers = {
            'Authorization': f'Bearer {config("PAYSTACK_SK")}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.get(url, headers=headers)
            paystack_response_data = response.json()

            if paystack_response_data['status'] and paystack_response_data['data']['status'] == 'success':
                # Implement your business logic for a successful payment here.
                order = Order.objects.get(reference=reference)  # Assuming reference is unique for Order
                order.status = 'processing'
                order.save()
                return Response({'status': 'success', 'message': 'Payment successfully verified', 'data': paystack_response_data['data']})
            else:
                return Response({'status': 'failed', 'message': 'Payment could not be verified'},
                                status=status.HTTP_400_BAD_REQUEST)

        except requests.exceptions.RequestException as e:
            return Response({'error': 'An error occurred while verifying the payment'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class OrderDetailAPIView(RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        id= self.id
        order = Order.objects.get(id=id)
        return order
    