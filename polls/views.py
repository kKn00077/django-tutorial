from django.http import Http404, HttpResponse, HttpResponseRedirect # 404페이지, response, redirect
from django.shortcuts import render, get_object_or_404 # view load, 404 단축 기능
from django.urls import reverse # 만약 stub 메서드를 사용한다면 활성화
from django.views import generic #제너릭 뷰

# from django.template import loader
from .models import Question, Choice

# Create your views here.

# 클래스 (4장 이후) - https://velog.io/@rosewwross/Django-Using-Generic-Views
# https://blog.naver.com/PostView.nhn?blogId=pjok1122&logNo=221609547295
# https://dowtech.tistory.com/4
# https://idlecomputer.tistory.com/28
# ListView, DetailView - 제너릭 뷰의 한 종류
# ListView - 개체 목록 표시 제너릭 뷰
# ListView 제네릭 뷰는 <app name>/<model name>_list.html

# DetailView - 특정 개체 유형에 대한 세부 정보 페이지 표시 제너릭 뷰
# DetailView 제너릭 뷰는 <app name>/<model name>_detail.html

class IndexView(generic.ListView): 
    # template_name 지정하지 않으면 <app name>/<model name>_list.html 로 장고 내부에서 유추시켜 해당 템플릿 적용
    template_name = 'polls/index.html' # 이미 있는 polls/index.html을 사용
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """ 마지막으로 게시된 5개의 질문 반환 """
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView): # detailView는 기본적으로 전달받은 값을 pk로 생각한다.
    model = Question # 모델을 넘겨서 전달받은 pk값을 사용해 객체를 템플릿에 넘기게 됨 (pk를 거치기 때문에 넘겨주는 객체는 한개뿐이다)
    # template_name 지정하지 않으면 <app name>/<model name>_detail.html 로 장고 내부에서 유추시켜 해당 템플릿 적용
    template_name = 'polls/detail.html' # 자동으로 생성되는 템플릿 대신 특정 템플릿 이름을 지정
    # 같은 DetailView를 사용하지만 다른 템플릿을 사용해 서로 다른 모습으로 보이게 함
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# 함수 (4장 이전)
def index(request): # request는 HttpRequest 개체
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    
    # template = loader.get_template('polls/index.html') - 단축기능 대신 원래의 HttpResponse를 사용할 경우 사용
    context = {
        'latest_question_list': latest_question_list,
    }

    # polls 앱 디렉토리 내부에 있는 templates 폴더의 하위 디렉토리/파일을 검색한다. polls라는 폴더 내의 index.html을 찾음
    # 즉 polls/templates/polls/index.html
    # 만약 templates 내에 하위 디렉토리가 없고 바로 index.html이 있다면
    # get_template('index.html') 로 수정해주면 됨
    # https://galid1.tistory.com/261
    return render(request, 'polls/index.html', context) # render(request객체, 템플릿명, context 사전형 객체(대신 선택적인수임))
    # 위의 구문과 같은 의미 return HttpResponse(template.render(context, request))

def detail(request, question_id):
    """
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist: # 검색이 일치하지 않아 반환되는 row가 없을 경우 
        raise Http404("Question does not exist") # 404에러 발생시켜서 404페이지로 redirect
    """
    #하단의 구문은 상단의 구문의 단축기능의 형태로 똑같은 동작을 한다.
    # 비슷한 함수로 get_list_or_404()가 있다.
    # 이 경우 get이 아니라 filter를 사용해 
    # 리스트에 아무 값이 없을 경우 404 페이지를 띄운다
    # https://velog.io/@ash3767/DoesNotExist
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question':question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # https://docs.djangoproject.com/ko/3.1/intro/tutorial04/
    try:
        print(request.POST)
        selected_choice = question.choice_set.get(pk=request.POST['choice']) # request.POST 값을 문자열로 반환, get 요청일 경우는 request.GET(이지만 명시적 표현을 위해 request.POST 사용)
    except (KeyError, Choice.DoseNotExist): # request.POST는 사전과 같은 객체({key:value})로 key값이 없으면 해당 에러가 발생된다.
        return render(request, 'polls/detail.html', {
            'question' : question,
            'error_message' : "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    # HttpResponseRedirect는 하나의 인수를 받는다
    # 이 때 인수는 재전송될 url
    # reverse 함수는 url을 하드코딩 하지 않게 도와준다.
    # 받은 인수(url name과 전달할 값)를 바탕으로 url 패턴을 찾아 해당 뷰를 가리키게 한다.
    # 이 코드에서는 reverse가 '/polls/투표한 value(choice_id(==pk))값/results/' 를 반환한다
    # https://chagokx2.tistory.com/50
    # https://ugaemi.github.io/django/Django-reverse-and-resolve/
