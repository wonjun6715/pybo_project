from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # CASADE는 계정이 삭제되면 계정과 연결된 Question 모델 데이터를 모두 삭제하라는 의미
    subject = models.CharField(max_length=200) # 글자 수를 제한하고 싶을 때는 CharField를 사용
    content = models.TextField() # 글자 수 제한이 없는 데이터
    create_date = models.DateTimeField() # 날짜, 시간 관련 속성은 DateTimeField 사용


    def __str__(self):
        return self.subject # 데이터 조회시 id가 아닌 제목을 표시

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # Answer 모델은 질문에 대한 답변이므로 Question 모델을 속성으로 가져야함
    # 모델을 속성으로 가지면 ForeignKey 이용, CASCADE는 종속이라는 뜻, 질문이 삭제되면 답변도 삭제 되어야 함
    content = models.TextField()
    create_date = models.DateTimeField()
