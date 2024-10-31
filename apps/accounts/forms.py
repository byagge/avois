# accounts/forms.py
from django import forms
from apps.users.models import User
from django.core.exceptions import ValidationError

# accounts/forms.py
from django import forms
from django.contrib.auth import authenticate

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise ValidationError("Passwords do not match.")
        return password_confirm


class LoginForm(forms.Form):
    username = forms.CharField(label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # Попытка аутентификации по username или email
        user = None
        if username_or_email and password:
            # Проверяем по имени пользователя
            user = authenticate(username=username_or_email, password=password)
            if not user:
                # Если пользователя по имени не найдено, ищем по email
                try:
                    user_with_email = User.objects.get(email=username_or_email)
                    user = authenticate(username=user_with_email.username, password=password)
                except User.DoesNotExist:
                    pass
            if not user:
                raise forms.ValidationError("Invalid username/email or password.")

        cleaned_data['user'] = user
        return cleaned_data


# accounts/forms.py
class PasswordResetForm(forms.Form):
    username = forms.CharField(label="Username or Email")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).first() or User.objects.filter(email=username).first()
        if not user:
            raise forms.ValidationError("User not found with this username/email.")
        return username

    def save(self):
        username = self.cleaned_data.get('username')
        new_password = self.cleaned_data.get('new_password')
        user = User.objects.filter(username=username).first() or User.objects.filter(email=username).first()
        user.set_password(new_password)
        user.save()
