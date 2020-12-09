from django.contrib import admin
from .models import Question, Choice
# Register your models here.
admin.site.register(Question) # Question의 데이터를 생성/수정/삭제할 수 있도록 등록
admin.site.register(Choice)