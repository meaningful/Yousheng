#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---------------------------------------------
    File  Name : AppUtils
    Author : agony
    Date : 2018/8/19
    Description: 
---------------------------------------------
"""
import hashlib


class EncodeUtils(object):
    @classmethod
    def encode(cls, str):
        hash_sha256 = hashlib.sha256()
        hash_sha256.update(bytes(str, encoding='utf-8'))
        hash_result = hash_sha256.hexdigest()
        return hash_result

