from django.shortcuts import render
from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse, HttpResponse
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
        "exp": int(datetime.datetime.now().timestamp()) + AUTH_EXPIRE
    }, settings.SECRET_KEY, "HS256").decode()  # 返回了一个字符串

# 过期时间
AUTH_EXPIRE = 8 * 60 * 60  # 8小时

# 认证函数
def authenticate(view):
    def wrapper(request:HttpRequest):
        # 用户传过来的token进行验证
        payload = request.META.get("HTTP_JWT")
        if not payload:  # 没有拿到，认证失败，返回401
            return HttpResponse(status=401)
        try:
            # 拿到之后验证token,同时验证过期时间
            payload = jwt.decode(payload, settings.SECRET_KEY, algorithms=["HS256"])
        except:
            return HttpResponse(status=401)

        try:
            # 验证通过将user_id注入到请求request中去
            user_id = payload.get("user_id", -1)
            user = User.objects.filter(pk=user_id).get()
            request.user = user
        except Exception as e:
            print(e)
            return HttpResponse(status=401)

        # 调用需要认证的函数，将注入user_id的请求传进去
        ret = view(request)
        return ret

    return wrapper

# 注册接口
def reg(request:HttpRequest):
    payload = simplejson.loads(request.body)  # 将提交的数据转成json格式
    # {'email': 'wangjie@qq.com', 'password': 'wangjie', 'name': 'wangjie'}
    try:
        # 将数据取出等一下要存到数据库中
        email = payload["email"]
        query = User.objects.filter(email=email)  # 邮箱验证

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

# 登录接口
def login(request:HttpRequest):
    payload = simplejson.loads(request.body)
    try:
        email = payload["email"]
        user = User.objects.filter(email=email).get()  # 查找数据库中是否有这个用户，有进行密码验证

        if bcrypt.checkpw(payload["password"].encode(), user.password.encode()):
            # 密码验证通过, 添加token信息
            token = gen_token(user.id)
            # 返回用户的相关信息
            res = JsonResponse({
                "user":{
                    "user_id": user.id,
                    "name": user.name,
                    "email": user.email,
                },
                "token": token
            })

            return res
        else:  # 验证失败，返回错误状态
            return HttpResponseBadRequest

    except Exception as e:
        return HttpResponseBadRequest()