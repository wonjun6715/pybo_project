from django.contrib import admin
from .models import Question

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

# Register your models here.
admin.site.register(Question, QuestionAdmin) # 장고 Admin에 Question 모델을 등록 => 이제부터 사용 가능해짐

