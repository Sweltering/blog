from django.shortcuts import render
from django.http import HttpRequest

def index(request:HttpRequest):
    """首页数据处理函数"""
    content = "本项目使用前后端分离，前端React，Django模板就没有必要使用了，耦合性太高，不利于协同开发。"
    department = {"技术部": "胡涛", "运营部": "张辽", "测试部": "李亮"}

    return render(
        request,
        "index.html",
        {"content": content, "department": department})