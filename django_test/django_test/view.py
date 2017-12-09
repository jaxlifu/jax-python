#!/usr/bin/env python
# coding=utf-8

from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context = {}
    context['hello'] = 'Hellow,World!'
    return render(request, 'index.html', context)


def test(request):
    return HttpResponse("Hello ,Django!")
