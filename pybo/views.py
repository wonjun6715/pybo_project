from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    """
    pybo 목록 출력
    """
    # 입력 인자
    page = request.GET.get('page', '1') # 페이지, 맨처음 불러오는 페이지가 1

    # 조회
    question_list = Question.objects.order_by('-create_date') # 데이터를 작성한 날짜의 역순(-)으로 조회하기 위해 order-by 함수 사용

    # 페이징 처리
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기

    # 페이징 마지막 페이지
    max_index = len(paginator.page_range)

    # 페이징 객체 생성
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'max_index' : max_index} # render 함수가 템플릿을 HTML로 변환하는 과정에서 사용되는 데이터 변수 context
    return render(request, 'pybo/question_list.html', context)
    # render 함수는 context에 있는 question_list를 pybo/question_list.html 파일에 적용하여 HTML 코드로 변환

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login') # 로그인이 되었는지를 우선 검사하여 1단계에서 본 오류를 방지
def answer_create(request, question_id): # request에는 question_detail.html에서 textarea에 입력된 데이터가 파이썬 객체에 담겨 넘어옴
    # question_id는 id 값이 넘어옴
    """
    pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user # 추가한 속성 author 적용
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question' : question, 'form' : form}
    return render(request, 'pybo/question_detail.html', context)

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

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    pybo 답변 수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    pybo 답변 삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)



