from rest_framework import generics
from .models import UserProfileModel
from .serializers import UserProfileSerializer
from rest_framework import permissions 
from rest_framework import parsers
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
class CreateUserProfileAPIView(generics.CreateAPIView):
    queryset = UserProfileModel.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data = request.data, instance =request.user.user_profile
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = {
            'status': status.HTTP_201_CREATED,
            'msg': 'profile created',
            'data': serializer.data
        }

        return Response(response)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    

class UpdateProfile(generics.UpdateAPIView):
    lookup_field = 'user_id'
    serializer_class = UserProfileSerializer
    queryset = UserProfileModel.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """Custom update with structured response & error handling"""
        try:
            instance = get_object_or_404(UserProfileModel, user_id=kwargs.get(self.lookup_field))

            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response({
                "status": "success",
                "message": "Profile updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)    

# class UpdateProfile(generics.UpdateAPIView):
#     lookup_field = 'user_id'
#     serializer_class = UserProfileSerializer
#     queryset = UserProfileModel.objects.all()
#     permission_classes = [permissions.IsAuthenticated]



class RetrieveProfile(generics.RetrieveAPIView):
    lookup_field = 'user_id'
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request, user_id=None):
        queryset = UserProfileModel.objects.get(user_id=user_id)
        serializer = UserProfileSerializer(queryset)
        res = {
            'msg': 'profile fetched successfully',
            'status': status.HTTP_200_OK,
            'data': serializer.data
        }
        return Response(res)