#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
from time import ctime, sleep


def music(name='长安忆'):
    for i in range(10):
        print('listing music %s ,%d times' % (name, i + 1))
        sleep(1)
    pass


def movie(name='动作枪战片'):
    for i in range(2):
        print('watcher music %s ,%d times' % (name, i + 1))
        sleep(5)
    pass


if __name__ == '__main__':
    thread1 = threading.Thread(target=music, args=('长安忆',))
    thread2 = threading.Thread(target=music, args=('故梦',))
    thread3 = threading.Thread(target=movie, args=('你的名字',))
    thread4 = threading.Thread(target=movie, args=('声之形',))
    thread5 = threading.Thread(target=movie, args=('我叫江小白',))
    threads = []
    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)
    threads.append(thread4)
    threads.append(thread5)
    for thread in threads:
        thread.start()
        thread.join()
    print('all over %s' % ctime())
