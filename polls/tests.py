import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question

# Create your tests here.
def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

# https://junlab.tistory.com/41
# https://smilelife12.github.io/WebCrawling10/
# https://developer.mozilla.org/ko/docs/Learn/Server-side/Django/Generic_views
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index')) # 테스트에서 시뮬레이션을 하기 위해 가상 클라이언트를 생성 -> 특정 페이지 접속
        self.assertEqual(response.status_code, 200) # 타입이 달라도 값이 같으면 True 반환 (==와 ===의 차이)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index')) # response 객체(다만 HttpResponse 타입이 아니라 WSGIRequest)를 반환함
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.") # assertContains = response를 이용해 페이지 내용을 불러와 뒤의 인자 내용값을 포함하고 있는지 비교, assertContains에 대해 더 알아보기
        self.assertQuerysetEqual(response.context['latest_question_list'], []) # https://eunjin3786.tistory.com/139 - 추후 assertQuerysetEqual에 대해 더 알아보기

    def test_future_question_and_past_question(self):
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response=self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        past_question = create_question(question_text='Past Question', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionModelTests(TestCase): # QuestionModelTests는 django.test.TestCase를 상속받는다. - https://wikidocs.net/28

    def test_was_published_recently_with_future_question(self): # 파이썬에서 메서드의 첫번째 매개변수는 관례적으로 self다. (self = 해당 메서드를 호출한 객체정보)
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        
        #assertIs는 TestCase의 메서드다. - https://itmining.tistory.com/126
        #assertIs(a, b)는 a is b를 체크한다.
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_old_question(self):
        # 하루보다 더 오래된 질문에 대해 False를 반환하는지 체크
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        # 아직 하루가 지나지 않은 질문에 대해 True를 반환하는지 체크
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def create_question(question_text, days):
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text,)

# django python shell에서의 테스트 방법 - https://docs.djangoproject.com/ko/3.1/intro/tutorial05/

"""
 테스트 구동 순서 정리
 1. python manage.py test polls - 앱 내에서 test를 찾는다.
 2. TestCase를 상속받은 클래스를 찾는다.
 3. 테스트용 DB 생성 (테스트 케이스 마다 이 db는 재설정 되어 초기화 된다.)
 4. 찾은 클래스 내에서 메서드명이 test로 시작하는 메서드를 찾아 실행

-테스트 클라이언트(Shell)-

(테스트 환경 구성 - test.py와는 다르게 Shell에서 할 경우 필요함)
from django.test.utils import setup_test_environment
setup_test_environment() - response의 추가적인 속성을 사용할 수 있게 템플릿 렌더러를 설치해줌
위의 메소드는 테스트용 DB를 생성하지는 않고 현재 커넥트된 DB를 사용
settings.py의 TIME_ZONE이 올바르지 않을 경우 결과 오류 발생할 수도 있음.

(테스트 클라이언트 클래스)
from django.test import Client - test.py에서는 TestCase에 있는 클라이언트를 사용한다.


https://velog.io/@teddybearjung/Djangotutorial05
"""

