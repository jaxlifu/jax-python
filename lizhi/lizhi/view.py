#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect

from Student.models import Student

import time
import json


def serializable_request(request):
    method = request.method
    POST = request.POST
    GET = request.GET
    body = request.body
    content_type = request.content_type
    COOKIES = request.COOKIES
    FILES = request.FILES
    META = request.META
    path = request.path
    path_info = request.path_info
    resolver_match = request.resolver_match
    content_params = request.content_params

    print(' request info is  ====> \n%s %s %s %s %s %s %s %s %s %s %s %s'
          % (method, POST, GET, "", content_type, COOKIES, FILES,
             META, path, path_info, resolver_match, content_params))

# 信息列表


def get_user_list(request):
    user_list = [{'message': 'user list is empty!'}]
    students = Student.objects.all()
    # serializable_request(request)
    if students.count() > 0:
        print('==== student count is %d' % (students.count()))
        user_list.clear()
        for item in students:
            user_list.append(json.loads(item.__str__()))
    # return HttpResponse(json.dumps(user_list))
    return render(request, 'infoList.html', {'list': json.dumps(user_list)})


def rename_image(number, userName, fileName):
    return '%s_%s_%s' % (number, userName, fileName)
    pass

# post上传信息


def upload_user_info(request):
    try:
        if request.method == 'POST':
            name = request.POST['name']
            mobile = request.POST['mobile']
            message = request.POST['message']
            number = request.POST['number']
            if 'image_current' in request.FILES:
                image_current = request.FILES['image_current']
                image_current.name = rename_image(
                    number, name, image_current.name)
            else:
                image_current = None

            if 'image_meeting' in request.FILES:
                image_meeting = request.FILES['image_meeting']
                image_meeting.name = rename_image(
                    number, name, image_meeting.name)
            else:
                image_meeting = None

            if 'image_school' in request.FILES:
                image_school = request.FILES['image_school']
                image_school.name = rename_image(
                    number, name, image_school.name)
            else:
                image_school = None

            if not Student.objects.filter(name=name):
                student = Student(name=name, message=message, number=number,
                                  mobile=mobile, image_current=image_current,
                                  image_meeting=image_meeting,
                                  image_school=image_school)
                student.save()
            else:
                Student.objects.filter(name=name).update(
                    name=name, message=message, number=number,
                    mobile=mobile, image_current=image_current,
                    image_meeting=image_meeting,
                    image_school=image_school)
            # return HttpResponse(json.dumps({'message': '上传信息成功!'}))
            return redirect('/getStudentList')
        else:
            # return HttpResponse(json.dumps({'message': '请以post方式上传信息!'}))
            return redirect('/index')
    except Exception as e:
        return HttpResponse(json.dumps({'message': '上传信息失败! %s' % e}))
    # finally:
    # serializable_request(request)

# 首页


def index(request):
    return render(request, 'index.html')

# 聚会时光


def metting(request):
    return render(request, 'metting.html')

# 上传信息


def upload(request):
    return render(request, 'upload.html')
