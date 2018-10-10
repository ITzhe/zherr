# /usr/bin/python
# -*- coding: utf-8 -*-
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect, HttpResponse
from  zherr import settings
import os
import re


class AuthMD(MiddlewareMixin):
    # 白名单
    white_list = ['/','/login/','/admin/','/server/status/']
    # black_list = ['/black/', ]  # 黑名单
    #
    # # 请求到达视图之前
    # def process_request(self, request):  # 必须叫process_request
    #     user = request.user  # 查看请求中是否含有user对象
    #     # user = request.session.get("username")
    #     url = request.path_info  # 路径是哪个
    #     print("url==============", url)
    #     if url in self.white_list or user:
    #         return  # 必须为空，为了后续的函数执行
    #     else:
    #         return redirect("/login/")  # 登录失败重定向到login页

    def process_request(self,request):
        request_url = request.path_info     # 请求的URL
        permisson_url = request.session.get('url')

        if request_url in self.white_list:
            return None

        if not permisson_url:
            return HttpResponse("您访问的页面异常，请联系管理员！")

        for i in permisson_url:
            # 根据 访问的URL去session中的权限列表去做正则匹配
            result = re.match(i,request_url)
            if result:
                return None
        else:
            return HttpResponse("没有访问的权限")



