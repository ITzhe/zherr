# /usr/bin/python
# -*- coding: utf-8 -*-
import salt.client
from saltstack import models
from django.shortcuts import render, HttpResponse,redirect

def Command(request):
    host_list = models.Host.objects.all().values("hostname")
    if request.method == "GET":
        return render(request, "deploy/command.html", {"host_list": host_list})

    ret_list =  request.POST.getlist("host")
    client_command = request.POST.get('command')

    local = salt.client.LocalClient()
    for h in ret_list:
        ret = local.cmd_async(h,client_command)

    return render(request,"deploy/command.html",{"host_list":host_list})