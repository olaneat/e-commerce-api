from .apiviews import CreateUserProfileAPIView, UpdateProfile, RetrieveProfile
from django.urls import path


app_name = 'user-profile'

urlpatterns = [
    path('create', CreateUserProfileAPIView.as_view(), name='create-profile'),
    path('<uuid:user_id>/update', UpdateProfile.as_view(), name='update-profile'),
    path('<uuid:user_id>/display', RetrieveProfile.as_view(), name='display-profile')

]
