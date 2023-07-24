from django.shortcuts import render
from .models import Question

def index(request):
    """
    pybo 목록 출력
    """
    question_list = Question.objects.order_by('-create_date') # 데이터를 작성한 날짜의 역순(-)으로 조회하기 위해 order-by 함수 사용
    context = {'question_list': question_list} # render 함수가 템플릿을 HTML로 변환하는 과정에서 사용되는 데이터 변수 context
    return render(request, 'pybo/question_list.html', context)
    # render 함수는 context에 있는 question_list를 pybo/question_list.html 파일에 적용하여 HTML 코드로 변환
