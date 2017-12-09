#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests


def keepSession():
    s = requests.Session()
    s.auth = ('user', 'pass')
    s.headers.update({'x-test': 'true'})
    s.get('http://httpbin.org/headers', headers={'x-test2': 'true'})
    r = s.get('http://httpbin.org/cookies', cookies={'from-my': 'browser'})
    print(r.text)
    # s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
    r = s.get('http://httpbin.org/cookies')
    print(r.text)
    pass


if __name__ == '__main__':
    #keepSession()
