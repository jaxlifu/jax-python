#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itchat
import logging


@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    logging.info(msg['Text'])
    pass


itchat.auto_login(hotReload=True)
itchat.run()
