from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator

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
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj} # render 함수가 템플릿을 HTML로 변환하는 과정에서 사용되는 데이터 변수 context
    return render(request, 'pybo/question_list.html', context)
    # render 함수는 context에 있는 question_list를 pybo/question_list.html 파일에 적용하여 HTML 코드로 변환

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

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
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question' : question, 'form' : form}
    return render(request, 'pybo/question_detail.html', context)
def question_create(request):
    """
    pybo 질문 등록
    """
    if request.method == 'POST': # 질문 등록화면에서 입력값을 채우고 <저장하기> 버튼을 누르면 POST 방식으로 요청되어 데이터 저장
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False) # commit=False는 임시저장을 의미, 실제 데이터는 아직 저장되지 않은 상태
            question.create_date = timezone.now()
            question.save() # 실제 저장
            return redirect('pybo:index')
    else: # 질문 목록 화면에서 <질문 등록하기> 버튼을 누르면 GET 방식으로 요청되어 질문 등록화면이 나타남
        form = QuestionForm() # request 메세지가 'GET'인 경우 호출
    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context)
