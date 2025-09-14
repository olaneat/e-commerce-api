from rest_framework.response import Response
from rest_framework import permissions 
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework import generics, viewsets, status
from .serializers import OrderSerializer, ItemSerializer, OrderListSerializer, VerifyPaymentSeializer
from .models import Order, Item
from django.conf import settings
from decouple import config
import requests
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
        serializer = OrderSerializer(data={'items': items_data, 'status': 'pending_payment'}, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            payment_intent =  f"pi_{order.id}"
            order.payment_intent_id = payment_intent
            order.save()
            # total_cost =
            # default= 
            payment_url = 'https://api.paystack.co/transaction/initialize'
            amount_in_kobo = int(order.total_amount * 100) 
            payload = {
                'reference': order.reference,
                'email': request.user.email,
                'amount': amount_in_kobo,
                "callback_url": "https://neatstorez.vercel.app/verify-payment"
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
                    order.status = 'processing'
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
                print(f"Paystack API error: {e}")
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
        print(f"Serializer errors: {serializer.errors}")
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
    queryset = Order.objects.all()


class DeleteOrderView(generics.DestroyAPIView):
    # lookup_field = 'id'
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()




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

# @csrf_exempt
# def verify_payment(request):
#     print(request.POST.get('reference'))
#     if request.method == 'POST':
#         reference = request.POST.get('reference')
#         if not reference:
#             return JsonResponse({'error': 'Reference is required'}, status=400)

#         # Paystack Verify Transaction API endpoint
#         url = f"https://api.paystack.co/transaction/verify/{reference}"
#         headers = {
#             'Authorization': f'Bearer {config("PAYSTACK_SK")}',
#             'Content-Type': 'application/json'
#         }

#         try:
#             response = requests.get(url, headers=headers)
#             response_data = response.json()

#             if response.status_code == 200 and response_data['data']['status'] == 'success':
#                 # Update Payment model
#                 payment = Payment.objects.get(ref=reference)
#                 payment.verified = True
#                 payment.save()

#                 # Update associated Order status
#                 order = Order.objects.get(reference=reference)  # Assuming reference is unique for Order
#                 order.status = Order.PROCESSING
#                 order.save()

#                 return JsonResponse({
#                     'status': 'success',
#                     'message': 'Payment and order verified',
#                     'data': response_data['data'],
#                     'order_status': order.status
#                 })
#             else:
#                 return JsonResponse({
#                     'status': 'failed',
#                     'message': 'Payment verification failed',
#                     'data': response_data.get('data', {})
#                 }, status=400)

#         except Payment.DoesNotExist:
#             return JsonResponse({'error': 'Payment not found'}, status=404)
#         except Order.DoesNotExist:
#             return JsonResponse({'error': 'Order not found'}, status=404)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Invalid request method'}, status=405)



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