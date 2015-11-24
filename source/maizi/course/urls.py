#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2015/11/3
@author: yopoing
course模块的url配置。
"""

from django.conf.urls import patterns, url

urlpatterns = patterns('course.views',
    url(r'^$', 'career_course', name='career_course'),
    url(r'(?P<short_name>\w{0,10})$', 'course', name='course'),
)
