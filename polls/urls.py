#https://blog.naver.com/kartmon/221881132114
from django.urls import path # https://cjh5414.github.io/understand-python-import-with-django-example/
from . import views # . == 현재 디렉토리==polls -> polls 하위에 있는 py 파일을 views.py import

 #만약 다른 앱에서 이름이 겹치는 url이 있을 경우를 대비한 이름공간
app_name = 'polls'

urlpatterns = [
    #ex: /polls/
    path('', views.IndexView.as_view(), name='index'), # name 속성을 통해 view를 식별한다
    #ex: /polls/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    #ex: /polls/5/resultss/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    #ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]