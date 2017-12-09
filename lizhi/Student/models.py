#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
import json

# Create your models here.

'''
姓名
学号
手机
高中照片
近期照片
聚餐照片
毕业感言

'''


class Student(models.Model):
    name = models.CharField(max_length=20, unique=True)
    mobile = models.CharField(max_length=11)
    number = models.IntegerField()
    message = models.CharField(max_length=1024, null=True)
    image_current = models.ImageField(upload_to='photos/', blank=True, null=True)
    image_meeting = models.ImageField(upload_to='photos/', blank=True, null=True)
    image_school = models.ImageField(upload_to='photos/', blank=True, null=True)

    class Meta:
        db_table = 'student'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return json.dumps(self, default=lambda obj: obj.__dict__)
