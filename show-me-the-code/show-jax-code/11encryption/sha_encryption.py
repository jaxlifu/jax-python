#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from hashlib import sha256
from hmac import HMAC


def encryption_password(password, salt=None):
    if not salt:
        salt = os.urandom(8)
    result = sha256(password.encode('utf-8') + salt).hexdigest()
    return salt, result
    pass


def validate_password(user, password):
    salt = user['salt']
    return sha256(password.encode('utf-8') + salt).hexdigest() == user['password']
    pass


if __name__ == '__main__':
    user = {'password': '', 'salt': b''}
    user['salt'], user['password'] = encryption_password('123456')
    result = validate_password(user, '123456')
    print(result)
