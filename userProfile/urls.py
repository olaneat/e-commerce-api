from .apiviews import CreateUserProfileAPIView, UpdateProfile
from django.urls import path


app_name = 'user-profile'

urlpatterns = [
    path('create', CreateUserProfileAPIView.as_view(), name='create-profile'),
    path('update//<uuid:id>', UpdateProfile.as_view(), name='update-profile')
]
