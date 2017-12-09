#!/usr/bin/env python
# coding=utf-8

from django.http import HttpResponse
from TestModel.models import Test

import json


def insert(request):
    try:
        insert = Test(name='google', age=24, number=20, _id=10)
        insert.save()
        result = Test.objects.get(_id=20)
        return HttpResponse(json.dumps(result, default=lambda obj: obj.__dict__))
    except Exception as e:
        return HttpResponse(json.dumps({"error": "%s" % e}))
    pass
