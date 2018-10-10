# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from saltstack import models
#
#
# class PermissionAdmin(admin.ModelAdmin):
#     list_display = ['title', 'url', 'name']
#     list_editable = ['url', 'name']


admin.site.register(models.Permission)
admin.site.register(models.User)
admin.site.register(models.Role)
# admin.site.register(models.Menu)