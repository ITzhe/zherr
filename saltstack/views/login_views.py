# /usr/bin/python
# -*- coding: utf-8 -*-

from saltstack  import models
from django.shortcuts import render, HttpResponse,redirect


def Login(request):
    if request.method == "GET":
        return render(request,"login.html")
    username = request.POST.get("username")
    password = request.POST.get("password")

    obj = models.User.objects.filter(username=username,passwrod=password).first()
    if obj:
        role = obj.role.job
        # 权限空列表
        permissions_list = []

        per = models.Role.objects.filter(job=role).first()
        permission_qset = per.permission.all()
        for i in permission_qset:
            permissions_list.append(i.url)

        # 将权限信息放到session

        request.session['url'] = permissions_list

        return redirect("/server/index/")

    return render(request, "login.html")