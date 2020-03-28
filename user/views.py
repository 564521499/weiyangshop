import base64
import json, jwt, time, hashlib
import random, redis
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponse, JsonResponse

from dtoken.views import maketoken
from tools.logging_check import logging_check
from .models import UserProfile, Address, WeiboUser
from .tasks import send_active_mail

# Create your views here.
# FBV基于函数的视图

from django.views.generic.base import View
r = redis.Redis(host='127.0.0.1', port=6379, db=0)


def users(request):
    #基于函数的视图fbv
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass

    return HttpResponse('--user test is ok--')


class Users(View):
    # CBV基于类的视图
    def get(self, request):
        return JsonResponse({'code': 200})

    def post(self, request):
        # request.POST只能获取post表单提交的数据
        # print(dict(request.POST))
        # request.body能获取除表单提交的其他数据
        # print(request.body)

        data = request.body
        print(data)
        if not data:
            result = {'code': '10101', 'error': {'message': 'Please give me data'}}
            return JsonResponse('result')
        #data 字节串, json.loads是否报错
        # python 3.6.4 不报错 3.5x建议decode
        json_obj = json.loads(data)
        username = json_obj.get('uname')
        email = json_obj.get('email')
        phone = json_obj.get('phone')
        password = json_obj.get('password')
        # 检查用户名是否可用
        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            result = {'code': '10102', 'error': 'The username is existed!'}
            return JsonResponse(result)
        # 密码哈希加密
        m = hashlib.md5()
        m.update(password.encode())
        # 创建用户
        try:
            # 创建用户,考虑是否重复插入
            user = UserProfile.objects.create(username=username, email=email,phone=phone, password=m.hexdigest())
        except Exception as e:
            result = {'code': '10102', 'error': 'The username is existed!'}
            return JsonResponse(result)
        # 生成token  (免登录一天)
        # 签发token - 官方jwt.encode()
        # {'code':200, 'username':'xxxx', 'data':{'token':xxxx}}
        token = maketoken(username)
        #TODO 发激活邮件
        random_int = random.randint(1000, 9999)
        code_str = username + '_' + str(random_int)
        code_str_bs = base64.urlsafe_b64encode(code_str.encode())
        # 将随机码组合,存储到redis中,可以扩展成只存储1-3天
        r.set('email_active_%s' % username, code_str)
        active_url = 'http://127.0.0.1:7000/dadashop/templates/active.html?code=%s' % (code_str_bs.decode())
        # 发邮件

        # 同步执行
        # send_active_mail(email,active_url)
        # delay 异步执行
        send_active_mail.delay(email, active_url)

        #  {'code':200,'data':{'token':xxx}},
        return JsonResponse({'code': 200, 'username': username, 'data': {'token': token.decode()}})

    def delete(self, request):
        pass


# 邮件发送配置

def users_active(request):
    # 激活用户
    if request.method != 'GET':
        result = {'code': 10104, 'error': {'message': 'Please use get !!'}}
        return JsonResponse(result)
    code = request.GET.get('code')
    if not code:
        result = {'code': 10104, 'error': {'message': 'Please give me code !!'}}
        return JsonResponse(result)
    try:
        # 解析code
        code_str = base64.urlsafe_b64decode(code.encode())
        # username_9999
        new_code_str = code_str.decode()
        username, rcode = new_code_str.split('_')
    except Exception as e:
        print(e)
        result = {'code': 10105, 'error': {'message': 'You code is wrong !!'}}
        return JsonResponse(result)
    old_data = r.get('email_active_%s' % username)
    if not old_data:
        result = {'code': 10106, 'error': {'message': 'You code is wrong !!'}}
        return JsonResponse(result)

    if code_str != old_data:
        result = {'code': 10107, 'error': {'message': 'You code is wrong !!'}}
        return JsonResponse(result)

    # 激活用户
    users = UserProfile.objects.filter(username=username)
    if not users:
        pass
    user = users[0]
    user.isActive = True
    user.save()

    # 删除redis缓存
    r.delete('email_active_%s' % (username))
    result = {'code': 200, 'data': {'message': '激活成功!'}}
    return JsonResponse(result)


class AddressView(View):
    @logging_check
    def get(self, request,username,id):
        # 获取地址
        user = request.myuser
        addressList = []
        all_add = Address.objects.filter(uid=user)
        for add in all_add:
            d = {'id': add.id, 'address': add.address, 'postcode': add.postcode,
                 'receiver_mobile': add.receiver_mobile, 'receiver': add.receiver,
                 'is_default': add.isDefault, 'tag': add.tag}
            addressList.append(d)
        result = {'code': 200, 'data': {'addresslist': addressList}}
        return JsonResponse(result)

    @logging_check
    def post(self, request,username,id):
        # 创建新地址
        #{"receiver":"王硕","address":"北京市北京市市辖区东城区哈哈","receiver_phone":"15788888888","postcode":"456489","tag":"家"}
        if username != request.myuser.username:
            # 请求不合法
            result = {'code': 10110, 'error':{'message':'The request is illegal'}}
            return JsonResponse(result)
        data = request.body
        json_obj = json.loads(data)
        receiver = json_obj.get('receiver')
        address = json_obj.get('address')
        receiver_mobile = json_obj.get('receiver_phone')
        postcode = json_obj.get('postcode')
        tag = json_obj.get('tag')
        user = request.myuser
        # 如果是第一次添加数据  则把当前数据设置为默认地址
        old_address = Address.objects.filter(uid=user)
        isdefault = False
        if not old_address:
            isdefault = True
            # 此次为第一次添加
        Address.objects.create(receiver=receiver,address=address,receiver_mobile=receiver_mobile,postcode=postcode,tag=tag,isDefault=isdefault,uid=user)
        addressList = []
        all_add = Address.objects.filter(uid=user)
        for add in all_add:
            d={'id':add.id,'address':add.address,'postcode':add.postcode,
               'receiver_mobile':add.receiver_mobile,'receiver':add.receiver,
               'is_default':add.isDefault,'tag':add.tag}
            addressList.append(d)
        result = {'code':200,'data':{'addresslist':addressList}}
        return JsonResponse(result)

class OAuthWeiboUrlView(View):
    def get(self,request):
        # 获取登录地址
        url = get_weibo_login_url()
        return JsonResponse({'code':200,'oauth_url':url})
class OAuthWeiboView(View):

    def get(self,request):
        #获取前端传来的 微博code
        code = request.GET.get('code')
        #向微博服务器发送请求 用code换取token
        #websocket
        try:
            user_info = get_access_token(code)
        except Exception as e:
            print('----get_access_token error')
            print(e)
            result = {'code':202, 'error': {'message': 'Weibo server is busy ~'}}
            return JsonResponse(result)

        #微博用户id
        wuid = user_info.get('uid')
        access_token = user_info.get('access_token')

        #查寻weibo用户表，判断是否是第一次光临
        try:
            weibo_user = WeiboUser.objects.get(wuid=wuid)
        except Exception as e:
            print('weibouser get error')
            #该用户第一次用微博登录
            #创建数据 & 暂时不绑定UserProfile
            WeiboUser.objects.create(access_token=access_token, wuid=wuid)
            data = {'code':'201', 'uid': wuid}
            return JsonResponse(data)
        else:
            #该用户非第一次微博登录
            #检查是否进行过绑定
            uid = weibo_user.uid
            if uid:
                #之前绑定过，则认为当前为正常登陆，签发token
                username = uid.username
                token = maketoken(username)
                result = {'code':200, 'username':username, 'data': {'token':token.decode()}}
                return JsonResponse(result)
            else:
                #之前微博登陆过，但是没有执行微博绑定注册
                data = {'code': '201', 'uid': wuid}
                return JsonResponse(data)

        # return JsonResponse({'code': 200, 'error': 'test'})


    def post(self,  request):
        #绑定注册
        #json 前端将weiboid 命名为uid POST 过来
        #返回值 跟 正常注册一样

        data = json.loads(request.body)
        uid = data.get('uid')
        email = data.get('email')
        phone = data.get('phone')
        username = data.get('username')
        password = data.get('password')
        m= hashlib.md5()
        m.update(password.encode())
        password_m = m.hexdigest()

        try:
            # 注册用户    事物
            with transaction.atomic():
                user = UserProfile.objects.create(username=username,phone=phone,email=email,password=password_m)
                weibo_user = WeiboUser.objects.get(wuid=uid)
                weibo_user.uid = user
                weibo_user.save()
        except Exception as e:
            print('---weibo register error---')
            print(e)
            return JsonResponse({'code':10115,'error':{'message':'The Username is existed'}})
        # 签发token
        # todo 发邮件?
        token = maketoken(username)
        result = {'code':200,'username':username,'data':{'token':token.decode()}}
        return JsonResponse(result)


    # return JsonResponse({'code':200})
def get_access_token(code):
    #向资源授权平台 换取token
    token_url = 'https://api.weibo.com/oauth2/access_token'
    post_data = {
        'client_id': settings.WEIBO_CLIENT_ID,
        'client_secret': settings.WEIBO_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': settings.WEIBO_REDIRECT_URI,
        'code':code
    }
    try:
        #向微博服务器发送post请求
        res = requests.post(token_url, data=post_data)
    except Exception as e:
        print('--weibo request error ')
        print(e)
        raise
    if res.status_code == 200:
        return json.loads(res.text)
    raise

def get_weibo_login_url():
    # response_type - code  代表启用授权码模式
    # scope 授权范围
    params = {'response_type':'code',
              'client_id':settings.WEIBO_CLIENT_ID,
              'redirect_uri':settings.WEIBO_REDIRECT_URI,
              'scope':''}
    weibo_url = 'https://api.weibo.com/oauth2/authorize?'
    url = weibo_url+urlencode(params)
    return url






