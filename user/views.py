from django.shortcuts import render
from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
import simplejson
from .models import User
import jwt
import datetime
from django.conf import settings
import bcrypt

# Create your views here.

# 生成token认证签名
def gen_token(user_id):
    return jwt.encode({
        "user_id": user_id,
        # 增加时间戳，判断是否需要重发token或者重新登陆
        "timestamp": int(datetime.datetime.now().timestamp())
    }, settings.SECRET_KEY, "HS256").decode()  # 返回了一个字符串

# 注册接口
def reg(request:HttpRequest):
    payload = simplejson.loads(request.body)  # 将提交的数据转成json格式
    # {'email': 'wangjie@qq.com', 'password': 'wangjie', 'name': 'wangjie'}
    try:
        # 将数据取出等一下要存到数据库中
        email = payload["email"]
        query = User.objects.filter(email=email)  # 邮箱验证
        print(query)
        if query:  # 查到了，说明已经注册，直接返回错误，没查到，继续下面存数据的操作
            return HttpResponseBadRequest()

        name = payload["name"]
        # 密码存储需要加密，使用加盐的方式
        password = bcrypt.hashpw(payload["password"].encode(), bcrypt.gensalt())

        # 创建User实例，存到数据库中
        user = User()
        user.name = name
        user.email = email
        user.password = password
        try:
            user.save()
            return JsonResponse({"token": gen_token(user.id)})  # 返回Json数据到前端
        except:
            raise  # 不管，抛出到下面一层去处理
    except Exception as e:
        return HttpResponseBadRequest()  # 出现异常，返回异常的实例
