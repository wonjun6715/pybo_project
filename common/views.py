from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm

def signup(request):
    """
    회원가입
    """
    if request.method == 'POST': # 새로운 사용자 생성
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username') # form.cleaned_data.get 함수는 회원가입 화면에서 입력한 값을 얻기 위해 사용되는 함수
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else: # GET 요청 -> common/signup.html 화면 반환
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})
