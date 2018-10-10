# /usr/bin/python
# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import render, HttpResponse,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import salt.client

from saltstack import models


def index(request):
    return render(request, "index.html")


def default(request):
    return render(request, "default.html")


def server_add(request):
    local = salt.client.LocalClient()

    if request.method == "GET":
        return render(request, 'server_add.html')

    host = request.POST.get("host").encode("utf-8")

    obj = models.Host.objects.filter(hostname=host)
    if obj:
        return HttpResponse("该主机已经存在")

    host_info = local.cmd(host, 'grains.items')

    local.cmd(host, 'saltutil.sync_modules')
    disk = local.cmd(host, 'disk.disk_info')[host]

    # 网络表信息
    ip_addr = host_info[host].get("ip4_interfaces")
    mac_addr = host_info[host].get("hwaddr_interfaces")

    # 主机信息
    cpu = host_info[host].get("num_cpus")
    memory = host_info[host].get("mem_total")
    os_relase = host_info[host].get("os")

    # 主机详情表信息
    kernelrelease = host_info[host].get("kernelrelease")
    osrelease = host_info[host].get("osrelease")
    serialnumber = host_info[host].get("serialnumber")
    saltversion = host_info[host].get("saltversion")
    cpu_info = host_info[host].get("cpu_model")

    with transaction.atomic():
        host_ret = models.Host.objects.create(hostname=host,
                                              cpu=cpu,
                                              memory=memory,
                                              os=os_relase,
                                              )

        host_info = models.HostInfo.objects.create(kernelrelease=kernelrelease,
                                                   serialnumber=serialnumber,
                                                   minion_version=saltversion,
                                                   osrelease=osrelease,
                                                   cpu_info=cpu_info,
                                                   host=host_ret,
                                                   )
        for d in disk:
            type = disk.get(d)[1]
            if type == 'S':
                type = "SCSI"
            size = disk.get(d)[0]
            models.Disk.objects.create(partition=d, disk_type=type, disk_size=size, hostinfo=host_info)

        for i in ip_addr:
            if i != 'lo':
                ip = ip_addr.get(i)[0]
                mac = mac_addr.get(i)
                models.Network.objects.create(ipaddr=ip, network_name=i, mac_addr=mac, host=host_ret)
    return redirect("/server/list")
    # return JsonResponse(host_info)


def server_del(request):
    # models.Host.objects.filter(hostname=hostname).delete()
    return redirect("/server/list/")


def server_list(request):
    # host_list = models.Host.objects.all()
    host_list = models.Host.objects.get_queryset().order_by('id')

    paginator = Paginator(host_list, 10)
    # paginator = Paginator(host_list, 20)
    # 每页显示几条数据

    #异常判断
    try:
        current_num = int(request.GET.get("page", 1))
    #  当前的页码数
    # 如果获取GET的页数，如果获取不到参数，这里默认显示第一页
        current_list = paginator.page(current_num)
    except EmptyPage:
        current_num = int(1)
        current_list = paginator.page(current_num)

    return render(request, "server_list.html", {
        "current_list":current_list,
        "paginator":paginator,
        "current_num": current_num,
    })


def network_edit(request, id):
    info_id = models.Network.objects.filter(pk=id).values('network_name').first()
    back_id =  models.Network.objects.filter(pk=id).values('host_id').first()

    net_name = info_id.get('network_name')  # eth1
    if request.method == "GET":
        return render(request, "network_edit.html", {"net_name": net_name})

    new_bandwidth = request.POST.get(net_name)
    models.Network.objects.filter(pk=id).update(bandwidth=new_bandwidth + 'M')
    back_url = "/server/list/info/" + str(back_id.values()[0])
    return redirect(back_url)


def room_edit(request, id):
    if request.method == "GET":
        return render(request,"room_edit.html")


    region = request.POST.get("region")
    principal = request.POST.get("principal")
    phone = request.POST.get("phone")
    cabinet = request.POST.get("cabinet")
    h = models.Room.objects.filter(pk=id).first().room_info.id
    back_url = "/server/list/info/" + str(h)

    models.Room.objects.filter(pk=id).update(region=region,principal=principal,phone=phone,cabinet=cabinet)
    # return HttpResponse("添加成功")
    return redirect(back_url)

    # InfoFormSet= forms.formset_factory(RoomEdit,extra=2,min_num=1)
    # if request.method == 'GET':
    #     formset = InfoFormSet()
    #     return render(request, "server_info.html", {'formset': formset})
    #
    # formset = InfoFormSet(request.POST)
    # if formset.is_valid():
    #     # print(formset.cleaned_data)  # 验证通过的数据
    #     flag = False  # 标志位
    #     for row in formset.cleaned_data:
    #         if row:  # 判断数据不为空
    #             # print(row)  # 它是一个字典
    #             # **表示将字典扩展为关键字参数
    #             res = models.Room.objects.create(**row)
    #             if res:  # 判断返回信息
    #                 flag = True


def server_info(request, id):
    host_info = models.HostInfo.objects.filter(pk=id).first()
    network_info = models.Host.objects.filter(pk=id).first()

    from saltstack.utils import has_permission
    if_has_permission = has_permission.has_permission(request)

    return render(request, "server_info.html", {"host_info": host_info,
                                                "network_info": network_info,
                                                "if_has_permission":if_has_permission,
                                                })

def server_status(request):
    local = salt.client.LocalClient()
    host_status = local.cmd('*', 'test.ping')
    for k,v in host_status.items():
        if v:
            models.Host.objects.filter(hostname=k).update(status=1)
        else:
            models.Host.objects.filter(hostname=k).update(status=0)

    return HttpResponse(host_status)
