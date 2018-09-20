"""proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from basic_app import views
from django.views.decorators.cache import never_cache

urlpatterns = [
    url(r'^timer/', views.start_Timer),
    url(r'^admin/', admin.site.urls),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^register/$', never_cache(views.register), name='register'),
    url(r'^elogin/', views.elogin),
    url(r'^$',never_cache(views.waiting), name='waiting'),
    url(r'^questions/$',views.question_panel,name='question_panel'),
    url(r'codingpage/(?P<id>\d+)/$',views.questions,name='questions'),
    url(r'codingpage/$',views.questions,name='questions'),
    url(r'leader/$',views.leader,name='leader'),
    url(r'instructions/$',never_cache(views.instructions),name='instructions'),
    url(r'retry/(?P<id>\d+)/$',views.retry,name='retry'),
    url(r'submissions/$',views.sub,name='sub'),
    url(r'^checkuse$',views.checkuser,name="checkuser"),
    url(r'^loadbuff$',views.loadbuff,name='loadbuff'),
    url(r'/',views.register, name='register'),

]
