# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Host(models.Model):
    hostname = models.CharField(max_length=32,unique=True,verbose_name="主机名")
    cpu = models.CharField(max_length=32,verbose_name="CPU")
    memory = models.CharField(max_length=32,verbose_name="内存")
    # os_type = ((0,"CentOS"),(1,"RedHat"),(2,"UbanTu"),(3,"SUSE"))
    # os = models.SmallIntegerField(choices=os_type,default=0,verbose_name="操作系统")
    os = models.CharField(max_length=32,default="CentOS",verbose_name="操作系统")
    status = models.BooleanField(default=False,verbose_name="是否在线")

class HostInfo(models.Model):
    cpu_info = models.CharField(max_length=32,verbose_name="CPU信息")
    kernelrelease = models.CharField(max_length=32,verbose_name="内核名称")
    message = models.TextField(max_length=255,null=True,blank=True,verbose_name="备注信息")
    serialnumber = models.CharField(max_length=128,verbose_name="序列号")
    minion_version = models.CharField(max_length=16,verbose_name="Minion版本")
    osrelease = models.CharField(max_length=32,verbose_name="操作系统版本")
    host = models.OneToOneField(to='Host',on_delete=models.CASCADE)


class Disk(models.Model):
    partition = models.CharField(max_length=32,verbose_name="对应分区")
    disk_type = models.CharField(max_length=32,verbose_name="硬盘类型")
    disk_size = models.CharField(max_length=32,verbose_name="硬盘大小")
    hostinfo = models.ForeignKey(to='HostInfo',on_delete=models.CASCADE)

class Network(models.Model):
    ipaddr = models.CharField(max_length=32,verbose_name="IP地址")
    network_name = models.CharField(max_length=32,verbose_name="网卡名称")
    mac_addr = models.CharField(max_length=32,verbose_name="MAC地址")
    bandwidth = models.CharField(max_length=10000,verbose_name="带宽",null=True,blank=True)
    host = models.ForeignKey(to='Host',on_delete=models.CASCADE)

class Room(models.Model):
    region = models.CharField(max_length=64,null=True,blank=True,verbose_name="机房/地区")
    principal = models.CharField(max_length=32,null=True,blank=True,verbose_name="负责人")
    phone = models.CharField(max_length=32,null=True,blank=True,verbose_name="联系方式")
    cabinet = models.CharField(max_length=32,null=True,blank=True,verbose_name="机柜位置")
    room_info = models.OneToOneField(to='HostInfo',on_delete=models.CASCADE)