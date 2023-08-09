from django import forms
from pybo.models import Question, Answer, Comment

class QuestionForm(forms.ModelForm):  # 이 같은 클래스를 장고 폼이라고 함, ModeelFrom을 상속받았으므로 모델 폼이라고 부름
    # 모델 폼 객체를 저장하면 연결된 모델의 데이터를 저장할 수 있음
    class Meta:  # 장고 모델 폼은 내부 클래스로 Meta 클래스를 반드시 가져야 하며, Meta 클래스에는 모델 폼이 사용할 모델과 모델의 필드들을 적음
        model = Question
        fields = ['subject', 'content']

        labels = {
            'subject' : '제목',
            'content' : '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content' : '답변내용',
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content' : '댓글내용',
        }
