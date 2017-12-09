#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
import random
import logging
import itchat
import json
import time
import re
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
from itchat.content import *
from baidu_img import *

logging.basicConfig(level=logging.INFO, handlers=[
                    logging.FileHandler('logger.log', 'w', 'utf-8')])

owner = ''


def tuling_chat(msg):
    if not msg:
        return
    api_url = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': '8edce3ce905a4c1dbb965e6b35c3834d',
        'userid': 'wechat-robot'
    }
    data['info'] = msg
    try:
        r = requests.post(api_url, data=data).json()
        return r.get('text')
    except Exception as e:
        logging.error(e)
        return
    pass


'''
MsgType	说明
1	文本消息
3	图片消息
34	语音消息
37	好友确认消息
40	POSSIBLEFRIEND_MSG
42	共享名片
43	视频消息
47	动画表情
48	位置消息
49	分享链接
50	VOIPMSG
51	微信初始化消息
52	VOIPNOTIFY
53	VOIPINVITE
62	小视频
9999	SYSNOTICE
10000	系统消息
10002	撤回消息
'''
# 自动回复机器人


@itchat.msg_register(INCOME_MSG,  isFriendChat=True, isGroupChat=True)
def tuling_reply(msg):
    msgType = msg.get('MsgType')
    content = msg.get('Content')
    fromUserName = msg.get('FromUserName')
    toUserName = msg.get('ToUserName')
    if fromUserName == owner and toUserName != 'filehelper':  # 自己发的消息直接忽略
        return
    logging.info(msg)

    default_reply = '哈哈哈哈,%s' % msg['Text']
    if msgType == 51:  # 初始化消息
        return
    elif msgType == 47:
        # elif msgType == 3:  # 图片或表情
        logging.info('表情的内容为%s' % content)
        cdnurl = re.findall(r'cdnurl = "(.*?)"', content, re.S)
        logging.info('cdnurl list%s' % cdnurl)
        filename = load_baidu_image(cdnurl[0])
        logging.info(filename)
        if msg['ToUserName'] == 'filehelper':  # 发送给文件传输助手
            itchat.send_image(fileDir=filename, toUserName='filehelper')
        else:
            itchat.send_image(fileDir=filename, toUserName=fromUserName)
        return
    elif msgType == 34:  # 语音消息
        reply = tuling_chat('收到一条语音消息')
    elif msgType == 62:  # 小视频
        reply = tuling_chat('收到一个小视频')
    else:
        reply = tuling_chat(msg['Text'])
    return reply or default_reply
    pass

# 群发助手


def friend_list():
    friendList = itchat.get_friends(update=True)[1:]  # 第一个是自己
    with open('friend.json', 'w', encoding='utf-8') as f:
        f.writelines(json.dumps(friendList, ensure_ascii=False))
    pass


def check_friend():
    pass


def chatrooms_list():
    rooms_list = itchat.get_chatrooms(update=True, contactOnly=False)
    with open('chatRoomsList.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(rooms_list, ensure_ascii=False))
    pass


def test():
    running = True
    while running:
        message = input(':>')
        if not message or message == 'bye':
            running = False
        print(tuling_chat(message))
    pass


if __name__ == '__main__':
    if not os.path.exists('download'):
        os.mkdir('download')
    init_headers()
    itchat.auto_login(hotReload=True)
    owner = itchat.get_friends()[0]['UserName']
    itchat.run()
