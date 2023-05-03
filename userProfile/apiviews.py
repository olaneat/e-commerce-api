from rest_framework import generics
from .models import UserProfileModel
from .serializers import UserProfileSerializer
from rest_framework import permissions 
from rest_framework import parsers
from rest_framework import status
from rest_framework.response import Response

class CreateUserProfileAPIView(generics.CreateAPIView):
    queryset = UserProfileModel.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            serializer = request.data, instance =request.user.user_profile
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = {
            'status': status.HTTP_201_CREATE,
            'msg': 'profile created',
            'header': headers,
            'data': serializer.data
        }

        return Response(response)
    


class UpdateProfile(generics.UpdateAPIView):
    lookup_field = 'user_id'
    serializer_class = UserProfileSerializer
    queryset = UserProfileModel.objects.all()
    permissions_classes = [permissions.IsAuthenticated]


class RetrieveProfile(generics.RetrieveAPIView):
    lookup_field = 'user_id'
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserProfileModel.objects.all()
