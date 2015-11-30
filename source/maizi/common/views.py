#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2015/11/3
@author: yopoing
Common模块View业务处理。
"""

from django.shortcuts import render,render_to_response,HttpResponse,RequestContext
from common.models import Links,RecommendedReading,UserProfile,Course,Lesson
from django.conf import settings
from django.core.paginator import Paginator,EmptyPage,InvalidPage,PageNotAnInteger
import json
from django.core.serializers import serialize
from django.db.models import Sum

def gloado(req):
    MEDIA_URL=settings.MEDIA_URL
    return locals()

# 首页
def index(request):
    links =Links.objects.all()
    recs=RecommendedReading.objects.all()
    userPiles=UserProfile.objects.all()
    return render(request, "common/index.html", locals())

def newBook(req):
    courses = getPage(req,Course.objects.all().order_by('-click_count'),8)
    return render_to_response('common/coures.html',locals(),context_instance=RequestContext(req))
def mostBook(req):
    list=Course.objects.all().values_list("id")
    courses = getPage(req,Course.objects.all(),8)
    les=Lesson.objects.filter(course__in=list).order_by('-play_count__sum').values('course__name','course__student_count').annotate(Sum('play_count'))
    lessions = getPage(req,les,8)
    print lessions
    return render_to_response('common/lession.html',locals())

def getCour(lession):
    courses=[]
    if lession:
        for le in lession:
            courses.append(le.get('course__name'))
    return courses
# SELECT `course`.`name`, `course`.`student_count`, SUM(`lesson`.`play_count`) AS `play_count__sum` FROM `lesson` INNER JOIN `course` ON ( `lesson`.`course_id` = `course`.`id` ) WHERE (`lesson`.`course_id`) IN (SELECT U0.`id` FROM `course` U0) GROUP BY `course`.`name`, `course`.`student_count` ORDER BY `play_count__sum` DESC
def hotBook(req):
    courses = getPage(req,Course.objects.all().order_by('-date_publish'),8)
    return render_to_response('common/coures_hot.html',locals())
def getPage(req,page_list,count_in_page):
    paginator=Paginator(page_list,count_in_page)
    try:
        page =int(req.POST.get('page',1))
        # print pa
        # page=int(req.GET.get('page',1))
        print page
        page_list=paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        page_list=paginator.page(1)
    return page_list


