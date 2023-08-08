from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question

@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문 등록
    """
    if request.method == 'POST': # 질문 등록화면에서 입력값을 채우고 <저장하기> 버튼을 누르면 POST 방식으로 요청되어 데이터 저장
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False) # commit=False는 임시저장을 의미, 실제 데이터는 아직 저장되지 않은 상태
            question.author = request.user # 추가한 속성 author 적용
            question.create_date = timezone.now()
            question.save() # 실제 저장
            return redirect('pybo:index')
    else: # 질문 목록 화면에서 <질문 등록하기> 버튼을 누르면 GET 방식으로 요청되어 질문 등록화면이 나타남
        form = QuestionForm() # request 메세지가 'GET'인 경우 호출
    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author: # 로그인한 사용자와 수정하려는 글쓴이가 다르다면
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question) # instance 매개변수에 question을 지정하면 기존 값을 폼에 채울 수 있음
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now() # 질문 수정일시를 현재일시로 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')