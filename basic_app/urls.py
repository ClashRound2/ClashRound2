from django.conf.urls import url
from basic_app import views

app_name = 'basic_app'


urlpatterns=[
    url(r'^questions/$',views.question_panel,name='question_panel'),
    url(r'codingpage/(?P<id>\d+)/$',views.questions,name='questions'),
    url(r'codingpage/$',views.questions,name='questions'),
    url(r'leader/$',views.leader,name='leader'),
    url(r'instructions/$',views.instructions,name='instructions'),
    url(r'retry/(?P<id>\d+)/$',views.retry,name='retry'),
    url(r'submissions/$',views.sub,name='sub'),
    url(r'^checkuse',views.checkuser,name="checkuser"),
    url(r'/', views.question_panel)
]
