# -*- coding: utf-8 -*-
from common.models import *
from django.shortcuts import render, redirect, HttpResponse,render_to_response,HttpResponseRedirect
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from django.db.models import Sum

# Create your views here.
def career_course(request):
    career_course_list = CareerCourse.objects.all()
    career_course_list = getPage(request, career_course_list, 9)
    return render(request, 'course/career_course.html', locals())

def getPage(request, page_list, count_in_page):
    paginator = Paginator(page_list, count_in_page)
    try:
        page = int(request.GET.get('page', 1))
        page_list = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        page_list = paginator.page(1)
    return page_list

def course(request, short_name):
    # 根据当前url传的值确定当前职业课程
    career_course = CareerCourse.objects.get(short_name=short_name)
    # 选出当前职业课程下的stages列表
    stages = Stage.objects.filter(career_course=career_course)
    for stage in stages:
        # 选出当前stage下的course
        courses = Course.objects.filter(stages=stage)
        # 为stage加上courses字段及内容
        setattr(stage, 'courses', courses)
        for course in stage.courses:
            # 算出每个课程下所有视频的长度
            course_length = Lesson.objects.filter(course=course).aggregate(Sum('video_length'))
            # 为couse加上course_length_hour和course_length_minute字段
            course_length_hour = course_length['video_length__sum']/3600
            course_length_minute = course_length['video_length__sum']%3600/60
            setattr(course, 'course_length_hour', course_length_hour)
            setattr(course, 'course_length_minute', course_length_minute)
    #算出当前职业课程下所有视频的长度
    career_video_length = Lesson.objects.filter(course__stages=stages).aggregate(Sum('video_length'))
    #把秒转换成分钟
    career_video_length_hour = career_video_length['video_length__sum']/3600
    return render(request, 'course/course.html', locals())
