#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---------------------------------------------
    File  Name : BussinessORMViews
    Author : agony
    Date : 2018/8/11
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


# <- 销售单 Begin ->
# 销售单编号		salesListID
# 客户名称		customName
# 客户编号		customID
# 客户余额【不可手工编辑】【非表字段， 只是页面展示的显示】		customBalance
# 采购单编号	默认为空	purchaseID
# 品种		category
# 拖车号		tractorID
# 挂车号		trailerID
# 司机		driverName
# 押运员		supercargo
# 数量  	【默认显示挂车余量】	count
# 单位 【非表字段， 只是页面展示的显示】	吨/立方米
# 单价		unitPrice
# 码表公里数		mileage
# 下单日期	orderDate
# 入库日期   storageDate
# 备注		comment
# 是否已开发票（是/否）		isInvoiced
# 本单是否入库（是/否）	未入库销售单可修改 ， 已入库销售单只能浏览不能修改。【分支业务：超级管理员可更改已入库的销售单信息 ， 不能删除】	isStoraged


class SalesList(Base):
    __tablename__ = 'BussinessModels_saleslist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    salesListID = Column(String(128))
    customName = Column(String(128))
    customID = Column(String(128))
    purchaseID = Column(String(128))
    category = Column(String(128))
    tractorID = Column(String(128))
    trailerID = Column(String(128))
    driverName = Column(String(128))
    supercargo = Column(String(128))
    count = Column(String(128))
    unitPrice = Column(String(128))
    mileage = Column(String(128))
    orderDate = Column(Date)
    storageDate = Column(Date)
    comment = Column(String(128))
    isInvoiced = Column(String(128))
    isStoraged = Column(String(128))


class SalesListDBUtils(object):
    IS_STORAGED_YES = "是"
    IS_STORAGED_NO = "否"
    IS_INVOICED_YES = "是"
    IS_INVOICED_NO = "否"
    IS_INVOICED_NA = "NA"

    @classmethod
    def add(cls, salesList):
        if not isinstance(salesList, SalesList):
            raise TypeError('The parameter salesList is not instance of the SalesList instance')
        session = DBSession()
        session.add(salesList)
        session.flush()
        new_item_id = salesList.id
        session.commit()
        session.close()
        return new_item_id

    @classmethod
    def delete(cls, delId):
        session = DBSession()
        item_to_del = session.query(SalesList).filter_by(id=delId).first()
        session.delete(item_to_del)
        session.commit()
        session.close()

    @classmethod
    def update(cls, updateId, salesList):
        if not isinstance(salesList, SalesList):
            raise TypeError('The parameter salesList is not instance of the CustomerManage instance')
        session = DBSession()

        item_to_update = session.query(SalesList).filter_by(id=updateId).first()
        item_to_update.salesListID = salesList.salesListID
        item_to_update.customName = salesList.customName
        item_to_update.customID = salesList.customID
        item_to_update.purchaseID = salesList.purchaseID
        item_to_update.category = salesList.category
        item_to_update.tractorID = salesList.tractorID
        item_to_update.trailerID = salesList.trailerID
        item_to_update.driverName = salesList.driverName
        item_to_update.supercargo = salesList.supercargo
        item_to_update.count = salesList.count
        item_to_update.unitPrice = salesList.unitPrice
        item_to_update.mileage = salesList.mileage
        item_to_update.orderDate = salesList.orderDate
        item_to_update.storageDate = salesList.storageDate
        item_to_update.comment = salesList.comment
        item_to_update.isInvoiced = salesList.isInvoiced
        item_to_update.sStoraged = salesList.isStoraged

        session.commit()
        session.close()

    @classmethod
    def queryAll(cls):
        session = DBSession()
        queryAll = session.query(SalesList).all()
        allSalesList = []
        for item in queryAll:
            salesList_json = json.dumps(object2dict(item), cls=DateEncoder)
            salesList = json.loads(salesList_json)
            allSalesList.append(salesList)
        session.close()
        return allSalesList

    @classmethod
    def queryAllSalesListByIsStoraged(cls, isStoraged):
        session = DBSession()
        queryAll = session.query(SalesList).filter(SalesList.isStoraged == isStoraged).all()
        allSalesList = []
        for item in queryAll:
            salesList_json = json.dumps(object2dict(item), cls=DateEncoder)
            salesList = json.loads(salesList_json)
            allSalesList.append(salesList)
        session.close()
        return allSalesList

    @classmethod
    def queryAllSalesListByDate(cls, isInvoiced, fromDate, deadline):
        session = DBSession()
        if isInvoiced == SalesListDBUtils.IS_INVOICED_NA:
            queryAll = session.query(SalesList).filter(SalesList.orderDate >= fromDate,
                                                       SalesList.orderDate <= deadline).all()
        else:
            queryAll = session.query(SalesList).filter(SalesList.isInvoiced == isInvoiced,
                                                       SalesList.orderDate >= fromDate,
                                                       SalesList.orderDate <= deadline).all()
        allSalesList = []
        for item in queryAll:
            salesList_json = json.dumps(object2dict(item), cls=DateEncoder)
            salesList = json.loads(salesList_json)
            allSalesList.append(salesList)
        session.close()
        return allSalesList

    @classmethod
    def getCount(cls):
        session = DBSession()
        allCount = session.query(SalesList).count()
        session.close()
        return allCount

    @classmethod
    def getSalesListIDByEditId(cls, editId):
        session = DBSession()
        item = session.query(SalesList).filter_by(id=editId).first()
        session.close()
        return item.salesListID


# <- 销售单 End ->


# <- 采购单 Begin ->
# 采购单编号	时间日期+流水ID	purchaseID
# 供货商		supplierName
# 品种		category
# 拖车号		tractorID
# 挂车号		trailerID
# 司机		driverName
# 押运员		supercargo
# 数量		count
# 单价		unitPrice
# 码表数		mileage
# 下单日期	orderDate
# 入库日期   storageDate
# 本单是否入库（是/否）	未入库采购单可修改 ， 已入库采购单只能浏览不能修改。【分支业务：超级管理员可更改已入库的采购单信息，不能删除】	isStoraged


class MaterialPurchase(Base):
    __tablename__ = 'BussinessModels_materialpurchase'

    id = Column(Integer, primary_key=True, autoincrement=True)
    purchaseID = Column(String(128))
    supplierName = Column(String(128))
    category = Column(String(128))
    tractorID = Column(String(128))
    trailerID = Column(String(128))
    driverName = Column(String(128))
    supercargo = Column(String(128))
    count = Column(String(128))
    unitPrice = Column(String(128))
    mileage = Column(String(128))
    orderDate = Column(Date)
    storageDate = Column(Date)
    isStoraged = Column(String(128))


class MaterialPurchaseDBUtils(object):
    IS_STORAGED_YES = "是"
    IS_STORAGED_NO = "否"

    @classmethod
    def add(cls, materialPurchase):
        if not isinstance(materialPurchase, MaterialPurchase):
            raise TypeError('The parameter materialPurchase is not instance of the MaterialPurchase instance')
        session = DBSession()
        session.add(materialPurchase)
        session.flush()
        new_item_id = materialPurchase.id
        session.commit()
        session.close()
        return new_item_id

    @classmethod
    def delete(cls, delId):
        session = DBSession()
        item_to_del = session.query(MaterialPurchase).filter_by(id=delId).first()
        session.delete(item_to_del)
        session.commit()
        session.close()

    @classmethod
    def update(cls, updateId, materialPurchase):
        if not isinstance(materialPurchase, MaterialPurchase):
            raise TypeError('The parameter materialPurchase is not instance of the MaterialPurchase instance')
        session = DBSession()

        item_to_update = session.query(MaterialPurchase).filter_by(id=updateId).first()
        item_to_update.purchaseID = materialPurchase.purchaseID
        item_to_update.supplierName = materialPurchase.supplierName
        item_to_update.category = materialPurchase.category
        item_to_update.tractorID = materialPurchase.tractorID
        item_to_update.trailerID = materialPurchase.trailerID
        item_to_update.driverName = materialPurchase.driverName
        item_to_update.supercargo = materialPurchase.supercargo
        item_to_update.count = materialPurchase.count
        item_to_update.unitPrice = materialPurchase.unitPrice
        item_to_update.mileage = materialPurchase.mileage
        item_to_update.orderDate = materialPurchase.orderDate
        item_to_update.storageDate = materialPurchase.storageDate
        item_to_update.isStoraged = materialPurchase.isStoraged

        session.commit()
        session.close()

    @classmethod
    def queryAll(cls):
        session = DBSession()
        queryAll = session.query(MaterialPurchase).all()
        allMaterialPurchase = []
        for item in queryAll:
            materialPurchase_json = json.dumps(object2dict(item), cls=DateEncoder)
            materialPurchase = json.loads(materialPurchase_json)
            allMaterialPurchase.append(materialPurchase)
        session.close()
        return allMaterialPurchase

    @classmethod
    def queryAllMaterialPurchaseByIsStoraged(cls, isStoraged):
        session = DBSession()
        queryAll = session.query(MaterialPurchase).filter(MaterialPurchase.isStoraged == isStoraged).all()
        allMaterialPurchase = []
        for item in queryAll:
            materialPurchase_json = json.dumps(object2dict(item), cls=DateEncoder)
            materialPurchase = json.loads(materialPurchase_json)
            allMaterialPurchase.append(materialPurchase)
        session.close()
        return allMaterialPurchase

    @classmethod
    def queryAllMaterialPurchaseByDate(cls, isStoraged, fromDate, deadline):
        session = DBSession()
        queryAll = session.query(MaterialPurchase).filter(
            MaterialPurchase.isStoraged == isStoraged,
            MaterialPurchase.orderDate >= fromDate,
            MaterialPurchase.orderDate <= deadline).all()

        allMaterialPurchase = []
        for item in queryAll:
            materialPurchase_json = json.dumps(object2dict(item), cls=DateEncoder)
            materialPurchase = json.loads(materialPurchase_json)
            allMaterialPurchase.append(materialPurchase)
        session.close()
        return allMaterialPurchase

    @classmethod
    def getCount(cls):
        session = DBSession()
        allCount = session.query(MaterialPurchase).count()
        session.close()
        return allCount

    @classmethod
    def getPurchaseIDByEditId(cls, editId):
        session = DBSession()
        item = session.query(MaterialPurchase).filter_by(id=editId).first()
        session.close()
        return item.purchaseID


# <- 采购单 End ->


# <- 车辆维修安排（统计）Begin ->
# vehicleMaintenanceManage【车辆维修安排（统计）】
# 类型（拖车/挂车）		vehicleType
# 拖车号/挂车号		vehicleID
# 维修时间		maintenanceDate
# 维修项目		maintenanceItems
# 费用		maintenanceCost
# 备注		maintenanceComment


class VehicleMaintenanceManage(Base):
    __tablename__ = 'BussinessModels_vehiclemaintenancemanage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    salesListID = Column(String(128))
    vehicleType = Column(String(128))
    vehicleID = Column(String(128))
    maintenanceDate = Column(Date)
    maintenanceItems = Column(String(128))
    maintenanceCost = Column(String(128))
    maintenanceComment = Column(String(128))
    wastageManage = Column(String(128))
    trailerID = Column(String(128))
    wastageCount = Column(String(128))


class VehicleMaintenanceManageDBUtils(object):
    @classmethod
    def add(cls, vehicleMaintenanceManage):
        if not isinstance(vehicleMaintenanceManage, VehicleMaintenanceManage):
            raise TypeError('The parameter vehicleMaintenanceManage is not instance of the '
                            'VehicleMaintenanceManage instance')
        session = DBSession()
        session.add(vehicleMaintenanceManage)
        session.flush()
        new_item_id = vehicleMaintenanceManage.id
        session.commit()
        session.close()
        return new_item_id

    @classmethod
    def delete(cls, delId):
        session = DBSession()
        item_to_del = session.query(VehicleMaintenanceManage).filter_by(id=delId).first()
        session.delete(item_to_del)
        session.commit()
        session.close()

    @classmethod
    def update(cls, updateId, vehicleMaintenanceManage):
        if not isinstance(vehicleMaintenanceManage, VehicleMaintenanceManage):
            raise TypeError('The parameter vehicleMaintenanceManage is not instance of the '
                            'VehicleMaintenanceManage instance')
        session = DBSession()

        item_to_update = session.query(MaterialPurchase).filter_by(id=updateId).first()
        item_to_update.salesListID = vehicleMaintenanceManage.salesListID
        item_to_update.vehicleType = vehicleMaintenanceManage.vehicleType
        item_to_update.vehicleID = vehicleMaintenanceManage.vehicleID
        item_to_update.maintenanceDate = vehicleMaintenanceManage.maintenanceDate
        item_to_update.maintenanceItems = vehicleMaintenanceManage.maintenanceItems
        item_to_update.maintenanceCost = vehicleMaintenanceManage.maintenanceCost
        item_to_update.maintenanceComment = vehicleMaintenanceManage.maintenanceComment
        item_to_update.wastageManage = vehicleMaintenanceManage.wastageManage
        item_to_update.trailerID = vehicleMaintenanceManage.trailerID
        item_to_update.wastageCount = vehicleMaintenanceManage.wastageCount

        session.commit()
        session.close()

    @classmethod
    def queryAll(cls):
        session = DBSession()
        queryAll = session.query(VehicleMaintenanceManage).all()
        allVehicleMaintenanceManage = []
        for item in queryAll:
            vehicleMaintenanceManage_json = json.dumps(object2dict(item), cls=DateEncoder)
            vehicleMaintenanceManage = json.loads(vehicleMaintenanceManage_json)
            allVehicleMaintenanceManage.append(vehicleMaintenanceManage)
        session.close()
        return allVehicleMaintenanceManage


# <- 车辆维修安排（统计）End ->


# <- 损耗校验 Begin ->
# 挂车号		trailerID
# 损耗量 （吨）	默认值为现余量	wastageCount


class WastageManage(Base):
    __tablename__ = 'BussinessModels_wastagemanage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    trailerID = Column(String(128))
    wastageCount = Column(String(128))


class WastageManageDBUtils(object):
    @classmethod
    def add(cls, wastageManage):
        if not isinstance(wastageManage, WastageManage):
            raise TypeError('The parameter wastageManage is not instance of the WastageManage instance')
        session = DBSession()
        session.add(wastageManage)
        session.flush()
        new_item_id = wastageManage.id
        session.commit()
        session.close()
        return new_item_id

    @classmethod
    def delete(cls, delId):
        session = DBSession()
        item_to_del = session.query(WastageManage).filter_by(id=delId).first()
        session.delete(item_to_del)
        session.commit()
        session.close()

    @classmethod
    def update(cls, updateId, wastageManage):
        if not isinstance(wastageManage, WastageManage):
            raise TypeError('The parameter wastageManage is not instance of the WastageManage instance')
        session = DBSession()

        item_to_update = session.query(WastageManage).filter_by(id=updateId).first()
        item_to_update.trailerID = wastageManage.trailerID
        item_to_update.wastageCount = wastageManage.wastageCount

        session.commit()
        session.close()

    @classmethod
    def queryAll(cls):
        session = DBSession()
        queryAll = session.query(WastageManage).all()
        allWastageManage = []
        for item in queryAll:
            allWastageManage_json = json.dumps(object2dict(item), cls=DateEncoder)
            wastageManage = json.loads(allWastageManage_json)
            allWastageManage.append(wastageManage)
        session.close()
        return allWastageManage


# <- 损耗校验 End ->


# <- 客户充值信息 Begin ->
# 客户名		customName
# 缴费时间		payTime
# 缴费金额		payAmount
# 余额 【计算出来的， 不能改】		balance


class CustomPaymentInfo(Base):
    __tablename__ = 'BussinessModels_custompaymentinfo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customName = Column(String(128))
    payTime = Column(Date)
    payAmount = Column(String(128))
    balance = Column(String(128))


class CustomPaymentInfoDBUtils(object):
    @classmethod
    def add(cls, customPaymentInfo):
        if not isinstance(customPaymentInfo, CustomPaymentInfo):
            raise TypeError('The parameter customPaymentInfo is not instance of the CustomPaymentInfo instance')
        session = DBSession()
        session.add(customPaymentInfo)
        session.flush()
        new_item_id = customPaymentInfo.id
        session.commit()
        session.close()
        return new_item_id

    @classmethod
    def delete(cls, delId):
        session = DBSession()
        item_to_del = session.query(CustomPaymentInfo).filter_by(id=delId).first()
        session.delete(item_to_del)
        session.commit()
        session.close()

    @classmethod
    def update(cls, updateId, customPaymentInfo):
        if not isinstance(customPaymentInfo, CustomPaymentInfo):
            raise TypeError('The parameter customPaymentInfo is not instance of the CustomPaymentInfo instance')
        session = DBSession()

        item_to_update = session.query(CustomPaymentInfo).filter_by(id=updateId).first()
        item_to_update.customName = customPaymentInfo.customName
        item_to_update.payTime = customPaymentInfo.payTime
        item_to_update.payAmount = customPaymentInfo.payAmount
        item_to_update.balance = customPaymentInfo.balance

        session.commit()
        session.close()

    @classmethod
    def queryAll(cls):
        session = DBSession()
        queryAll = session.query(CustomPaymentInfo).all()
        allCustomPaymentInfo = []
        for item in queryAll:
            customPaymentInfo_json = json.dumps(object2dict(item), cls=DateEncoder)
            customPaymentInfo = json.loads(customPaymentInfo_json)
            allCustomPaymentInfo.append(customPaymentInfo)
        session.close()
        return allCustomPaymentInfo

# <- 客户充值信息 End ->
