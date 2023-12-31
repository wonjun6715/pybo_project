from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question') # CASADE는 계정이 삭제되면 계정과 연결된 Question 모델 데이터를 모두 삭제하라는 의미
    subject = models.CharField(max_length=200) # 글자 수를 제한하고 싶을 때는 CharField를 사용
    content = models.TextField() # 글자 수 제한이 없는 데이터
    create_date = models.DateTimeField() # 날짜, 시간 관련 속성은 DateTimeField 사용
    modify_date = models.DateTimeField(null=True, blank=True) # 질문을 언제 수정했는지 확인, 질문 수정일시
    voter = models.ManyToManyField(User, related_name='voter_question') # 추천인 추가
    # 하나의 질문에 여러명이 추천할 수 있고, 한 명이 여러개의 질문에 추천할 수 있으므로 N:N 관계를 의미하는 ManyToManyField 사용
    hater = models.ManyToManyField(User, related_name='hater_question') # 싫어요 기능 추가


    def __str__(self):
        return self.subject # 데이터 조회시 id가 아닌 제목을 표시

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # Answer 모델은 질문에 대한 답변이므로 Question 모델을 속성으로 가져야함
    # 모델을 속성으로 가지면 ForeignKey 이용, CASCADE는 종속이라는 뜻, 질문이 삭제되면 답변도 삭제 되어야 함
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True) # blank=True의 의미는 form.is_vaild()를 통한 입력 폼 데이터 검사시 값이 없어도 된다는 의미
                                                              # 답변 수정일시, 수정일시는 수정한 경우에만 생성되는 데이터이므로 조건 지정
    voter = models.ManyToManyField(User, related_name='voter_answer')
    hater = models.ManyToManyField(User, related_name='hater_answer')

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 댓글 글쓴이
    content = models.TextField() # 댓글 내용
    create_date = models.DateTimeField() # 댓글 작성일시
    modify_date = models.DateTimeField(null=True, blank=True) # 댓글 수정일시
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE) # 이 댓글이 달린 질문
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE) # 이 댓글이 달린 답변