from django.conf.urls import url, include
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


app_name = 'myapp'

urlpatterns = [
    #url(r'^$', views.HomePage.as_view(), name='Home'),


    #url(r'^profile/$', views.IndexView.as_view(), name='all-images'),
    #url(r'^upload/$', views.Upload.as_view(), name='upload'),
    #url(r'^image/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='get-image'),

    #url(r'^registration/$', views.Registration.as_view(), name='registration'),

    #url(r'^login/$', views.Login.as_view(), name='login'),


    url(r'^logout/$', views.Logout.as_view(), name='logout'),

    # ------------------------- Sheko's Habd ----------------------------------

    url(r'^$', views.HomePage.as_view(), name='Home'),
    url(r'^registration/$', views.Registration.as_view(), name='registration'),

    path('<str:user>/home/', views.UserHome.as_view(), name='UserHome'),


]
