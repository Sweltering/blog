from django.shortcuts import render
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest,  HttpResponseNotFound
from user.views import authenticate
from .models import Post, Content
from user.models import User
import simplejson
import datetime
import math

# Create your views here.

# 提交博文功能
# 需要先认证用户
@authenticate
def pub(request:HttpRequest):
    # 创建post表和content表的实例，提交的数据要保存在数据库中
    post = Post()
    content = Content()
    try:
        payload = simplejson.loads(request.body)

        post.title = payload["title"]  # title放到post的实例中
        post.author = User(id=request.user.id)  # user_id之前验证的时候注入到请求中的，放到post的实例中
        post.pubdate = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))  # 现在提交发布的时间
        post.save()  # 现在才保存到数据库中

        content.content = payload["content"]  # 内容放到content实例中
        content.post = post
        content.save()

        return JsonResponse({"post_id": post.id})
    except Exception as  e:
        print(e)
        return HttpResponseBadRequest()

# 查询博文功能
def get(request:HttpRequest, id):
    try:
        id = int(id)
        post = Post.objects.get(pk=id)  # 在数据库中找这个id的文章
        print(post)
        if post:  # 在数据库中有这个id，就将相关返回前端
            return JsonResponse({
                "post": {
                    "post_id": post.id,
                    "title": post.title,
                    "author_name": post.author.name,
                    "author_id": post.author_id,
                    "pubdate": post.pubdate.timestamp(),
                    "content": post.content.content
                }
            })
    except Exception as e:
        print(e)
        return HttpResponseNotFound()

# 显示博文列表功能
def getall(request:HttpRequest):
    # 页码
    try:
        # 从请求的查询字符串中找到页码
        page = int(request.GET.get("page", 1))
        page = page if page > 0 else 1
    except:
        page = 1

    # 每一页显示的行数
    try:
        # 从请求的查询字符串中找到y页码行数
        size = int(request.GET.get("size", 20))
        size = size if size > 0 and size < 101 else 20
    except:
        size = 20

    # 根据请求的页码和行数做处理后返回前端
    try:
        start = (page - 1) * size  # 页码1,行数20,数据库中的文章从0开始查,页码2,行数20,开始20,依次类推
        posts = Post.objects.order_by("-id") # 按照id倒排
        count = posts.count()  # 总博文数
        posts = posts[start:start+size]  # 将查到的内容以页码和行数过滤后当作结果集
        # 将查到的结果集返回前端
        return JsonResponse({
            "posts": [
                {
                    "post_id": post.id,
                    "title": post.title
                } for post in posts
            ],
            "pagination": {  # 分页的信息
                "page": page,
                "size": size,
                "count": count,
                "pages": math.ceil(count/size)
            }
        })

    except Exception as e:
        print(e)
        return HttpResponseNotFound()