from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from django.utils import timezone

def index(request):
    """
    pybo 목록 출력
    """
    question_list = Question.objects.order_by('-create_date') # 데이터를 작성한 날짜의 역순(-)으로 조회하기 위해 order-by 함수 사용
    context = {'question_list': question_list} # render 함수가 템플릿을 HTML로 변환하는 과정에서 사용되는 데이터 변수 context
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
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # textarea에 입력된 데이터가 넘어온 값을 추출하기 위한 코드
    # POST 형식으로 전송된 form 데이터 항목 중 name이 content인 값을 의미
    return redirect('pybo:detail', question_id=question.id)
