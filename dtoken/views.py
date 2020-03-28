import json
import time
import jwt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from user.models import UserProfile


def tokens(request):
    # 登录
    if not request.method == 'POST':
        result = {'code':'10201','error':'Please user POST'}
        return JsonResponse(result)
    data = request.body
    json_obj = json.loads(data)
    username = json_obj.get('username')
    password = json_obj.get('password')
    # todo 检查参数是否存在
    if not username:
        result = {'code': '10201', 'error': 'No username'}
        return JsonResponse(result)
    if not password:
        result = {'code': '10201', 'error': 'No password'}
        return JsonResponse(result)

    # 查询用户
    user = UserProfile.objects.filter(username = username)
    if not user:
        result = {'code': '10202', 'error': 'username or password is wrong'}
        return JsonResponse(result)
    user = user[0]
    import hashlib
    m = hashlib.md5()
    m.update(password.encode())
    if m.hexdigest() != user.password:
        result = {'code': '10203', 'error': 'username or password is wrong'}
        return JsonResponse(result)

    #　生成token
    token = maketoken(username)
    result = {'code': '200', 'username':username,'data':{'token':token.decode()}}
    return JsonResponse(result)

def maketoken(username,expire = 3600*24):
    # 注册成功登录后,签发token,默认一天有效期
    key = settings.JWT_TOKEN_KEY
    now = time.time()
    payload = {'username':username,'exp':now+expire}
    return jwt.encode(payload,key,algorithm='HS256')
