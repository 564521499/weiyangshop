from django.conf.urls import url

from dtoken import views

urlpatterns=[
    url(r'^$',views.tokens)
]