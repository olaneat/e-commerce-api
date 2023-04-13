from rest_framework import serializers
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from .models import UserProfileModel
from register.models import CustomUser

class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField(source='user.username')
    uuid= serializers.UUIDField(format='hex_verbose', source="user.id", read_only=True)
    queryset = UserProfileModel.objects.all()
    
    
    parser_classes = (
        MultiPartParser,
        FormParser
    )

    class Meta: 
        model = UserProfileModel,
        fields = '__all__'

    def create(self, validated_data, instance=None):
        if 'user' in validated_data:
            user = validated_data.pop('user')
        else:
            user = CustomUser.objects.create(**validated_data)
        profile = UserProfileModel.objects.update_or_create(
            user=user, defaults=validated_data
        )
        return profile
