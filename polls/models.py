import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
# https://docs.djangoproject.com/ko/3.1/intro/tutorial02/ - 모델의 활성화
# https://brownbears.tistory.com/443 - 마이그레이션 정의
class Question(models.Model): #DB를 클래스 형식으로 선언해서 내부에 스키마 구조로 구성, 쉽게 말하면 VO같은 형식
    question_text = models.CharField(max_length=200) # question_text 라는 varchar(200) 컬럼
    pub_date = models.DateTimeField('date published') # pub_date 라는 datetime 컬럼, date published 라는 이름을 장고 내에서 명시

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #on_delete = 제약조건, 제약조건을 CASCADE로 해서 외래키 컬럼 설정
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

# python manage.py makemigrations polls - 마이그레이션 파일 생성
# python manage.py sqlmigrate polls 0001 - 마이그레이션 파일 생성 + 적용된 쿼리