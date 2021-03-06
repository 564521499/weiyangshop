from django.conf.urls import url

from user import views

urlpatterns=[
    # http://127.0.0.1:8000/v1/users
    # url(r'^$',views.users),
    url(r'^$',views.Users.as_view()),
    #
    url(r'^/activation$',views.users_active),

    # http://127.0.0.1:8000/v1/users/wangshuo9/adress/0
    url(r'^/(?P<username>\w+)/address/(?P<id>\d+)$',views.AddressView.as_view()),

    # 用于前端获取 微博登录地址
    url(r'^/weibo/authorization$',views.OAuthWeiboUrlView.as_view()),

    #接收前端微博code
    url(r'^/weibo/users$', views.OAuthWeiboView.as_view())
]



from django.db.models import Count

# v1/tokens POST    创建token -登录
# v1/authorization POST 创建校验- 登录