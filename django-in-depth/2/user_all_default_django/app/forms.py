from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, \
                                      AdminPasswordChangeForm, \
                                        SetPasswordForm, PasswordChangeForm, PasswordResetForm
from django.forms import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import login

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'is_staff', 'is_superuser', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        """
        email = self.cleaned_data.get('email')
        user = User.objects.get(email=email)
        login(request, user)
        """
        return super().clean()