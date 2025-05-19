import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise ValidationError("A senha deve ter pelo menos 8 caracteres.")
        if not re.search(r"[A-Z]", password1):
            raise ValidationError(
                "A senha deve conter pelo menos uma letra maiúscula."
            )
        if not re.search(r"[a-z]", password1):
            raise ValidationError(
                "A senha deve conter pelo menos uma letra minúscula."
            )
        if not re.search(r"[0-9]", password1):
            raise ValidationError("A senha deve conter pelo menos um número.")
        if not re.search(r"[\W_]", password1):
            raise ValidationError(
                "A senha deve conter pelo menos um caractere especial."
            )
        return password1
