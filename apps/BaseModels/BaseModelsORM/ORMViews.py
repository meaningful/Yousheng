#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---------------------------------------------
    File  Name : ORMViews
    Author : agony
    Date : 2018/7/29
    Description: 
---------------------------------------------
"""
import datetime
import json
from sqlalchemy import Column, String, Integer, Date, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

# 创建ORM对象的基类
Base = declarative_base()

# 初始化数据库连接:
# '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
engine = create_engine('mysql+pymysql://root:WLW2017test@47.93.228.118:3306/yousheng')

# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


# Datetime 类型json序列化
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


# Python类转dict
def object2dict(obj):
    # convert object to a dict
    d = {}
    # d['__class__'] = obj.__class__.__name__
    # d['__module__'] = obj.__module__
    d.update(obj.__dict__)
    if '_sa_instance_state' in d:
        del d['_sa_instance_state']
    return d

# def dict2object(d):
#     # convert dict to object
#     if '__class__' in d:
#         class_name = d.pop('__class__')
#         module_name = d.pop('__module__')
#         module = __import__(module_name)
#         class_ = getattr(module, class_name)
#         args = dict((key.encode('ascii'), value) for key, value in d.items())  # get args
#         inst = class_(**args)  # create new instance
#     else:
#         inst = d
#     return inst

# <- 公司人员管理表 Begin ->
# 编号		staffID
# 姓名		staffName
# 身份证号		idNumber
# 入职时间		hiredate
# 职务		position
# 照片		photo
# 人员简历		resume
# 人员类别	（办公室/司机/押运员）	category


class StaffManage(Base):
    __tablename__ = 'BaseModels_staffmanage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    staffID = Column(String(128))
    staffName = Column(String(128))
    idNumber = Column(String(128))
    hiredate = Column(Date)
    position = Column(String(128))
    photo = Column(String(128))
    resume = Column(String(128))
    category = Column(String(128))


# StaffManage 数据库操作类
class StaffManageDBUtils(object):
    def add(self, staff):
        if not isinstance(staff, StaffManage):
            raise TypeError('The parameter staff is not instance of the StaffManage instance')
        session = DBSession()
        session.add(staff)
        session.commit()
        session.close()

    def queryAll(self):
        session = DBSession()
        queryAll = session.query(StaffManage).all()
        allStaffs = []
        for item in queryAll:
            staff_json = json.dumps(object2dict(item), cls=DateEncoder)
            staff = json.loads(staff_json)
            allStaffs.append(staff)
        session.close()
        return allStaffs

# <- 公司人员管理表 End ->

# <- 用户管理表 Begin ->
# 用户名		userName
# 密码		userPassword


class UserManage(Base):
    __tablename__ = 'BaseModels_usermanage'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    userName = Column(String(128))
    userPassword = Column(String(128))



