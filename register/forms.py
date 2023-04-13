'''from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import SignupForm, SetPasswordField, PasswordField
from django.contrib.auth import get_user_model
from .models import CustomUser
from allauth.account.forms import SetPasswordField, PasswordField


class CustomUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20)
    confirm_phone_number = forms.CharField(max_length=20, label='confirm phone number')
    address = forms.CharField(widget=forms.TextInput(attrs={'col':2, 'row':3}))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.confirm_phone_number = self.cleaned_data['confirm_phone_number']
        user.address = self.cleaned_data['address']
        user.save()
        return user


    class Meta:
        model = get_user_model()
        fields = ('first_name', 'email')


class CustomChangeUserForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = "__all__"

'''