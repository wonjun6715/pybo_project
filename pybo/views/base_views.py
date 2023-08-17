from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count

from ..models import Question

def index(request):
    """
    pybo 목록 출력
    """
    # 입력 인자
    page = request.GET.get('page', '1') # 페이지, 맨처음 불러오는 페이지가 1
    kw = request.GET.get('kw', '') # 검색어
    so = request.GET.get('so', 'recent') # 정렬 기준

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date') # 추천수가 같으면 최신순으로
    elif so == 'popular':
        question_list = Question.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date') # 답변수가 같으면 최신순으로
    else: # recent
        question_list = Question.objects.order_by('-create_date')

    # 조회

    if kw:
        # kw는 keyword를 의미, Q함수의 icontains(대소문자 구분 x)는 kw가 각각의 내용에 포함되어있는지를 의미
        question_list = question_list.filter( # filter 함수에서 모델 필드에 접근하려면 __ 사용
            Q(subject__icontains=kw) | # 제목 검색
            Q(content__icontains=kw) | # 내용 검색
            Q(author__username__icontains=kw) | # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw) # 답변 글쓴이 검색
        ).distinct()

    # 페이징 처리
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기

    # 페이징 마지막 페이지
    max_index = len(paginator.page_range)

    # 페이징 객체 생성
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'max_index': max_index, 'page': page, 'kw': kw} # render 함수가 템플릿을 HTML로 변환하는 과정에서 사용되는 데이터 변수 context
    return render(request, 'pybo/question_list.html', context)
    # render 함수는 context에 있는 question_list를 pybo/question_list.html 파일에 적용하여 HTML 코드로 변환

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)