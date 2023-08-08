from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from ..models import Question

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