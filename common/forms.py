from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    email = forms.EmailField(label='이메일') # 기본적으로 가지고 있는 속성에 email 속성 추가

    class Meta:
        model = User
        fields = ("username", "email")