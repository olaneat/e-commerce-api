from rest_framework.response import Response
from rest_framework import permissions 
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
# from .models import OrderReference
from .serializers import CreateOrderSerializer


class CreateOrderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateOrderSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = request.data
        response = {
            'success': True,
            'message': "payment initiated",
            'status_code': status.HTTP_201_CREATED,
            'reference': serializer.data.get('id', None),
        }
        return Response(response)