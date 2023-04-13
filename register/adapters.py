from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=False ):
        data = form.cleaned_data
        user.email = data.get('email')
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.confirm_phone_number = data.get('confirm_phone_number')
        user.phone_number = data.get('phone_number')
        user.location = data.get('location')
        if 'password1' in data:
            user.set_password(data['password1'])
        else:
            user.set_unable_password()
        self.populate_email(self, request)
        if commit:
            user.save()
        return user