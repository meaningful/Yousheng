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
from sqlalchemy import Column, String, Integer, Date, create_engine, func, asc, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from apps.AppUtils import DataUtils, DateUtils
from apps.BaseModels.BaseModelsORM.BaseORMViews import TractorManage, TrailerManage, TractorManageDBUtils, TrailerManageDBUtils

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
    IS_NA = "NA"

    @classmethod
    def add(cls, salesList):
        if not isinstance(salesList, SalesList):
            raise TypeError('The parameter salesList is not instance of the SalesList instance')
        session = DBSession()
        session.add(salesList)
        session.flush()
        new_item_id = salesList.id

        # 销售单入库时，更新最新余额
        if salesList.isStoraged == SalesListDBUtils.IS_STORAGED_YES:
            latestCustomPaymentInfo = session.query(CustomPaymentInfo).order_by(desc(CustomPaymentInfo.payTime),
                                                                                desc(CustomPaymentInfo.id)).filter(
                CustomPaymentInfo.customName == salesList.customName).first()
            if latestCustomPaymentInfo:
                latestCustomPaymentInfo.balance = DataUtils.strNumToDeciaml(
                    latestCustomPaymentInfo.balance) - DataUtils.countSaleListPrice(salesList.count, salesList.unitPrice)

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
        item_to_update.isStoraged = salesList.isStoraged

        # 销售单入库时，更新最新余额
        if salesList.isStoraged == SalesListDBUtils.IS_STORAGED_YES:
            latestCustomPaymentInfo = session.query(CustomPaymentInfo).order_by(desc(CustomPaymentInfo.payTime),
                                                                                desc(CustomPaymentInfo.id)).filter(
                CustomPaymentInfo.customName == salesList.customName).first()
            if latestCustomPaymentInfo:
                latestCustomPaymentInfo.balance = DataUtils.strNumToDeciaml(
                    latestCustomPaymentInfo.balance) - DataUtils.countSaleListPrice(salesList.count, salesList.unitPrice)

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
    def queryAllSalesListForCustomerBillList(cls, customName, fromDate, deadline):
        session = DBSession()

        queryAll = session.query(SalesList).order_by(asc(SalesList.storageDate)).filter(
            SalesList.customName == customName,
            SalesList.storageDate >= fromDate,
            SalesList.storageDate <= deadline).all()

        allSalesList = []
        for item in queryAll:
            salesList_json = json.dumps(object2dict(item), cls=DateEncoder)
            salesList = json.loads(salesList_json)
            allSalesList.append(salesList)
        session.close()
        return allSalesList

    @classmethod
    def queryAllSalesListByDate(cls, customName, category, fromDate, deadline):
        session = DBSession()
        # if isInvoiced == SalesListDBUtils.IS_INVOICED_NA:
        #     queryAll = session.query(SalesList).order_by(asc(SalesList.orderDate)).filter(
        #             SalesList.orderDate >= fromDate,
        #             SalesList.orderDate <= deadline).all()
        # else:
        #     queryAll = session.query(SalesList).order_by(asc(SalesList.orderDate)).filter(
        #             SalesList.isInvoiced == isInvoiced,
        #             SalesList.orderDate >= fromDate,
        #             SalesList.orderDate <= deadline).all()

        # 1. 仅 customName 不为空
        if customName.strip() and not category.strip() and not fromDate.strip() and not deadline.strip():
            queryAll = session.query(SalesList).order_by(desc(SalesList.orderDate)).filter(
                SalesList.customName == customName,
                SalesList.isStoraged == SalesListDBUtils.IS_STORAGED_YES).all()
        # 2. 仅 category 不为空
        elif not customName.strip() and category.strip() and not fromDate.strip() and not deadline.strip():
            queryAll = session.query(SalesList).order_by(desc(SalesList.orderDate)).filter(
                SalesList.category == category,
                SalesList.isStoraged == SalesListDBUtils.IS_STORAGED_YES).all()
        # 3. 仅 date 不为空
        elif not customName.strip() and not category.strip() and fromDate.strip() and deadline.strip():
            queryAll = session.query(SalesList).order_by(desc(SalesList.orderDate)).filter(
                SalesList.orderDate >= fromDate,
                SalesList.orderDate <= deadline,
                SalesList.isStoraged == SalesListDBUtils.IS_STORAGED_YES).all()
        # 4. 仅 customName 为空
        elif not customName.strip() and category.strip() and fromDate.strip() and deadline.strip():
            queryAll = session.query(SalesList).order_by(desc(SalesList.orderDate)).filter(
                SalesList.category == category,
                SalesList.orderDate >= fromDate,
                SalesList.orderDate <= deadline,
                SalesList.isStoraged == SalesListDBUtils.IS_STORAGED_YES).all()
        # 5. 仅 category 为空
        elif customName.strip() and not category.strip() and fromDate.strip() and deadline.strip():
            queryAll = session.query(SalesList).order_by(desc(SalesList.orderDate)).filter(
                SalesList.customName == customName,
                SalesList.orderDate >= fromDate,
                SalesList.orderDate <= deadline,
                SalesList.isStoraged == SalesListDBUtils.IS_STORAGED_YES).all()
        # 6. 仅 date 为空
        elif customName.strip() and category.strip() and not fromDate.strip() and not deadline.strip():
            queryAll = session.query(SalesList).order_by(desc(SalesList.orderDate)).filter(
                SalesList.customName == customName,
                SalesList.category == category,
                SalesList.isStoraged == SalesListDBUtils.IS_STORAGED_YES).all()
        # 7.查询条件全部不为空
        elif customName.strip() and category.strip() and fromDate.strip() and deadline.strip():
            queryAll = session.query(SalesList).order_by(desc(SalesList.orderDate)).filter(
                SalesList.customName == customName,
                SalesList.category == category,
                SalesList.orderDate >= fromDate,
                SalesList.orderDate <= deadline,
                SalesList.isStoraged == SalesListDBUtils.IS_STORAGED_YES).all()
        # 8.查询条件全部为空则查询所有已入库销售单
        elif not customName.strip() and not category.strip() and not fromDate.strip() and not deadline.strip():
            queryAll = session.query(SalesList).order_by(desc(SalesList.orderDate)).filter(
                SalesList.isStoraged == SalesListDBUtils.IS_STORAGED_YES).all()

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
    def getCountToday(cls, today):
        session = DBSession()
        allCount = session.query(SalesList).filter(SalesList.orderDate == today).count()
        session.close()
        return allCount

    @classmethod
    def getSalesListIDByEditId(cls, editId):
        session = DBSession()
        item = session.query(SalesList).filter_by(id=editId).first()
        session.close()
        return item.salesListID

    # 查询最早入库销售单的日期
    @classmethod
    def getEarliestStorageDate(cls):
        session = DBSession()
        earliestStorageDate = session.query(func.min(SalesList.storageDate)).all()
        session.close()
        return earliestStorageDate[0][0]

    # 查询最近入库销售单的日期
    @classmethod
    def getLatestStorageDate(cls):
        session = DBSession()
        latestStorageDate = session.query(func.max(SalesList.storageDate)).all()
        session.close()
        return latestStorageDate[0][0]


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
    def queryAllMaterialPurchaseByDate(cls, supplierName, category, fromDate, deadline):
        session = DBSession()
        # 1. 仅 supplierName 不为空
        if supplierName.strip() and not category.strip() and not fromDate.strip() and not deadline.strip():
            queryAll = session.query(MaterialPurchase).order_by(desc(MaterialPurchase.orderDate)).filter(
                MaterialPurchase.supplierName == supplierName,
                MaterialPurchase.isStoraged == MaterialPurchaseDBUtils.IS_STORAGED_YES).all()
        # 2. 仅 category 不为空
        elif not supplierName.strip() and category.strip() and not fromDate.strip() and not deadline.strip():
            queryAll = session.query(MaterialPurchase).order_by(desc(MaterialPurchase.orderDate)).filter(
                MaterialPurchase.category == category,
                MaterialPurchase.isStoraged == MaterialPurchaseDBUtils.IS_STORAGED_YES).all()
        # 3. 仅 date 不为空
        elif not supplierName.strip() and not category.strip() and fromDate.strip() and deadline.strip():
            queryAll = session.query(MaterialPurchase).order_by(desc(MaterialPurchase.orderDate)).filter(
                MaterialPurchase.orderDate >= fromDate,
                MaterialPurchase.orderDate <= deadline,
                MaterialPurchase.isStoraged == MaterialPurchaseDBUtils.IS_STORAGED_YES).all()
        # 4. 仅 supplierName 为空
        elif not supplierName.strip() and category.strip() and fromDate.strip() and deadline.strip():
            queryAll = session.query(MaterialPurchase).order_by(desc(MaterialPurchase.orderDate)).filter(
                MaterialPurchase.category == category,
                MaterialPurchase.orderDate >= fromDate,
                MaterialPurchase.orderDate <= deadline,
                MaterialPurchase.isStoraged == MaterialPurchaseDBUtils.IS_STORAGED_YES).all()
        # 5. 仅 category 为空
        elif supplierName.strip() and not category.strip() and fromDate.strip() and deadline.strip():
            queryAll = session.query(MaterialPurchase).order_by(desc(MaterialPurchase.orderDate)).filter(
                MaterialPurchase.supplierName == supplierName,
                MaterialPurchase.orderDate >= fromDate,
                MaterialPurchase.orderDate <= deadline,
                MaterialPurchase.isStoraged == MaterialPurchaseDBUtils.IS_STORAGED_YES).all()
        # 6. 仅 date 为空
        elif supplierName.strip() and category.strip() and not fromDate.strip() and not deadline.strip():
            queryAll = session.query(MaterialPurchase).order_by(desc(MaterialPurchase.orderDate)).filter(
                MaterialPurchase.supplierName == supplierName,
                MaterialPurchase.category == category,
                MaterialPurchase.isStoraged == MaterialPurchaseDBUtils.IS_STORAGED_YES).all()
        # 7.查询条件全部不为空
        elif supplierName.strip() and category.strip() and fromDate.strip() and deadline.strip():
            queryAll = session.query(MaterialPurchase).order_by(desc(MaterialPurchase.orderDate)).filter(
                MaterialPurchase.supplierName == supplierName,
                MaterialPurchase.category == category,
                MaterialPurchase.orderDate >= fromDate,
                MaterialPurchase.orderDate <= deadline,
                MaterialPurchase.isStoraged == MaterialPurchaseDBUtils.IS_STORAGED_YES).all()
        # 8.查询条件全部为空则查询所有已入库采购单
        elif not supplierName.strip() and not category.strip() and not fromDate.strip() and not deadline.strip():
            queryAll = session.query(MaterialPurchase).order_by(desc(MaterialPurchase.orderDate)).filter(
                MaterialPurchase.isStoraged == MaterialPurchaseDBUtils.IS_STORAGED_YES).all()

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
    def getCountToday(cls, today):
        session = DBSession()
        allCount = session.query(MaterialPurchase).filter(MaterialPurchase.orderDate == today).count()
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
# 维修类型       maintainType
# 维修项目		maintenanceItems
# 费用		maintenanceCost
# 备注		maintenanceComment


class VehicleMaintenanceManage(Base):
    __tablename__ = 'BussinessModels_vehiclemaintenancemanage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicleType = Column(String(128))
    vehicleID = Column(String(128))
    maintenanceDate = Column(Date)
    maintainType = Column(String(32))
    maintenanceItems = Column(String(128))
    maintenanceCost = Column(String(128))
    maintenanceComment = Column(String(128))


class VehicleMaintenanceManageDBUtils(object):

    MAINTAIN_TYPE_ALL = "ALL"
    MAINTAIN_TYPE_REGULAR = "年检"
    VEHICLE_TYPE_TRAILER = "挂车"
    VEHICLE_TYPE_TRACTOR = "拖车"

    @classmethod
    def add(cls, vehicleMaintenanceManage):
        if not isinstance(vehicleMaintenanceManage, VehicleMaintenanceManage):
            raise TypeError('The parameter vehicleMaintenanceManage is not instance of the '
                            'VehicleMaintenanceManage instance')
        session = DBSession()
        session.add(vehicleMaintenanceManage)
        session.flush()
        new_item_id = vehicleMaintenanceManage.id

        # 更新车辆年检时间
        if VehicleMaintenanceManageDBUtils.MAINTAIN_TYPE_REGULAR == vehicleMaintenanceManage.maintainType:
            if VehicleMaintenanceManageDBUtils.VEHICLE_TYPE_TRACTOR == vehicleMaintenanceManage.vehicleType:
                item = session.query(TractorManage).filter(
                    TractorManage.tractorID == vehicleMaintenanceManage.vehicleID).first()
                if item:
                    item.annualInspectionTime = vehicleMaintenanceManage.maintenanceDate
                    TractorManageDBUtils.updateBytractorID(item)

            if VehicleMaintenanceManageDBUtils.VEHICLE_TYPE_TRAILER == vehicleMaintenanceManage.vehicleType:
                item = session.query(TrailerManage).filter(
                    TrailerManage.trailerID == vehicleMaintenanceManage.vehicleID).first()
                if item:
                    item.annualInspectionTime = vehicleMaintenanceManage.maintenanceDate
                    TrailerManageDBUtils.updateBytrailerID(item)

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
            raise TypeError('The parameter ehicleMaintenanceManage is not instance of the '
                            'VehicleMaintenanceManage instance')
        session = DBSession()

        item_to_update = session.query(VehicleMaintenanceManage).filter_by(id=updateId).first()
        item_to_update.vehicleType = vehicleMaintenanceManage.vehicleType
        item_to_update.vehicleID = vehicleMaintenanceManage.vehicleID
        item_to_update.maintenanceDate = vehicleMaintenanceManage.maintenanceDate
        item_to_update.maintainType = vehicleMaintenanceManage.maintainType
        item_to_update.maintenanceItems = vehicleMaintenanceManage.maintenanceItems
        item_to_update.maintenanceCost = vehicleMaintenanceManage.maintenanceCost
        item_to_update.maintenanceComment = vehicleMaintenanceManage.maintenanceComment

        # 更新车辆年检时间
        if VehicleMaintenanceManageDBUtils.MAINTAIN_TYPE_REGULAR == vehicleMaintenanceManage.maintainType:
            if VehicleMaintenanceManageDBUtils.VEHICLE_TYPE_TRACTOR == vehicleMaintenanceManage.vehicleType:
                item = session.query(TractorManage).filter(
                    TractorManage.tractorID == vehicleMaintenanceManage.vehicleID).first()
                if item:
                    item.annualInspectionTime = vehicleMaintenanceManage.maintenanceDate
                    TractorManageDBUtils.updateBytractorID(item)

            if VehicleMaintenanceManageDBUtils.VEHICLE_TYPE_TRAILER == vehicleMaintenanceManage.vehicleType:
                item = session.query(TrailerManage).filter(
                    TrailerManage.trailerID == vehicleMaintenanceManage.vehicleID).first()
                if item:
                    item.annualInspectionTime = vehicleMaintenanceManage.maintenanceDate
                    TrailerManageDBUtils.updateBytrailerID(item)

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

    @classmethod
    def queryMaintenanceByType(cls, maintainType):
        session = DBSession()
        queryAll = session.query(VehicleMaintenanceManage).filter(
                            VehicleMaintenanceManage.maintainType == maintainType).all()
        allMaintenance = []
        for item in queryAll:
            maintenance_json = json.dumps(object2dict(item), cls=DateEncoder)
            maintenance = json.loads(maintenance_json)
            allMaintenance.append(maintenance)
        session.close()
        return allMaintenance


# <- 车辆维修安排（统计）End ->


# <- 损耗校验 Begin ->
# 挂车号		trailerID
# 损耗量 （吨）	默认值为现余量	wastageCount
# 定损日期   checkDate
# 损耗比率   wastageRatio


class WastageManage(Base):
    __tablename__ = 'BussinessModels_wastagemanage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    trailerID = Column(String(128))
    wastageCount = Column(String(128))
    checkDate = Column(Date)
    wastageRatio = Column(String(128))


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
        item_to_update.checkDate = wastageManage.checkDate
        item_to_update.wastageRatio = wastageManage.wastageRatio

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

    @classmethod
    def queryMonthWastage(cls, trailerID, fromDate, deadline):
        session = DBSession()
        # 查询该挂车在某个时间段的采购总量
        queryAllPurchase = session.query(MaterialPurchase).filter(MaterialPurchase.trailerID == trailerID,
                                                                  MaterialPurchase.isStoraged == MaterialPurchaseDBUtils.IS_STORAGED_YES,
                                                                  MaterialPurchase.storageDate >= fromDate,
                                                                  MaterialPurchase.storageDate <= deadline).all()
        totalOfPurchase = BusinessViewUtils.getTotalOfPurchase(queryAllPurchase)

        # 查询该挂车在某个时间段的损耗总量
        queryAllWastage = session.query(WastageManage).filter(WastageManage.trailerID == trailerID,
                                                              WastageManage.checkDate >= fromDate,
                                                              WastageManage.checkDate <= deadline).all()

        totalOfWastage = BusinessViewUtils.getTotalOfWastage(queryAllWastage)

        # 查询最近充值记录，作为结果集
        latestWastage = session.query(WastageManage).order_by(desc(WastageManage.checkDate),
                                                              desc(WastageManage.id)).filter(
            WastageManage.trailerID == trailerID).first()
        wastageRatio = BusinessViewUtils.computeWastageRatio(totalOfWastage, totalOfPurchase)

        # 计算最新的损耗比率，作为返回结果集
        latestWastage.wastageRatio = wastageRatio
        latestWastage.wastageCount = str(totalOfWastage)

        allWastage = []
        monthWastage_json = json.dumps(object2dict(latestWastage), cls=DateEncoder)
        monthWastage = json.loads(monthWastage_json)
        allWastage.append(monthWastage)

        # 注意，查询时不要进行 session.commit() ,否则会将已有记录进行更新掉
        session.close()
        return allWastage

    # # 根据定损日期月份查询求和
    # @classmethod
    # def queryMonthWastageByMonth(cls, month):
    #     session = DBSession()
    #     queryAll = session.query(WastageManage).filter(WastageManage.checkDate.like(month)).all()
    #     allMonthWastage = []
    #     for item in queryAll:
    #         allMonthWastage.append(int(item.wastageCount))
    #     session.close()
    #     return sum(allMonthWastage)

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
        # 所有销售单价格总和
        queryAllSaleList = session.query(SalesList).filter(SalesList.customName == customPaymentInfo.customName,
                                                           SalesList.isStoraged == SalesListDBUtils.IS_STORAGED_YES).all()
        # 所有充值总额
        queryAllCustomPaymentInfo = session.query(CustomPaymentInfo).filter(
            CustomPaymentInfo.customName == customPaymentInfo.customName).all()

        # 最近充值记录
        latestCustomPaymentInfo = session.query(CustomPaymentInfo).order_by(desc(CustomPaymentInfo.payTime),
                                                                            desc(CustomPaymentInfo.id)).filter(
            CustomPaymentInfo.customName == customPaymentInfo.customName).first()

        # 充值时计算并更新最近充值记录的余额
        latestCustomPaymentInfo.balance = BusinessViewUtils.getTotalOfPayAmount(
            queryAllCustomPaymentInfo) - BusinessViewUtils.getTotalOfAllSalelist(queryAllSaleList)

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
        # item_to_update.balance = customPaymentInfo.balance
        session.flush()
        # 所有销售单价格总和
        queryAllSaleList = session.query(SalesList).filter(SalesList.customName == customPaymentInfo.customName,
                                                           SalesList.isStoraged == SalesListDBUtils.IS_STORAGED_YES).all()
        # 所有充值总额
        queryAllCustomPaymentInfo = session.query(CustomPaymentInfo).filter(
            CustomPaymentInfo.customName == customPaymentInfo.customName).all()

        # 最近充值记录
        latestCustomPaymentInfo = session.query(CustomPaymentInfo).order_by(desc(CustomPaymentInfo.payTime),
                                                                            desc(CustomPaymentInfo.id)).filter(
            CustomPaymentInfo.customName == customPaymentInfo.customName).first()

        # 充值时计算并更新最近充值记录的余额
        latestCustomPaymentInfo.balance = BusinessViewUtils.getTotalOfPayAmount(
            queryAllCustomPaymentInfo) - BusinessViewUtils.getTotalOfAllSalelist(queryAllSaleList)

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

    @classmethod
    def queryAllLatestByCustomName(cls, customName):
        session = DBSession()
        allCustomPaymentInfo = []

        latestCustomPaymentInfo = session.query(CustomPaymentInfo).order_by(desc(CustomPaymentInfo.payTime),
                                                                            desc(CustomPaymentInfo.id)).filter(
            CustomPaymentInfo.customName == customName).first()

        if latestCustomPaymentInfo:
            customPaymentInfo_json = json.dumps(object2dict(latestCustomPaymentInfo), cls=DateEncoder)
            customPaymentInfo = json.loads(customPaymentInfo_json)
            allCustomPaymentInfo.append(customPaymentInfo)

        session.close()
        return allCustomPaymentInfo


# <- 客户充值信息 End ->


class BusinessViewUtils(object):

    @classmethod
    def getAllSalesListStorageDateMinAndMax(cls):
        dateFromTo = []
        session = DBSession()

        # 查询最早入库销售单的日期
        earliestStorageDate = session.query(func.min(SalesList.storageDate)).all()
        dateFromTo.append(earliestStorageDate[0][0])

        # 查询最近入库销售单的日期
        latestStorageDate = session.query(func.max(SalesList.storageDate)).all()
        dateFromTo.append(latestStorageDate[0][0])

        return dateFromTo

    @classmethod
    def getTotalOfAllSalelist(cls, queryAll):
        allSaleListTotal = []
        for item in queryAll:
            salesList_json = json.dumps(object2dict(item), cls=DateEncoder)
            salesList = json.loads(salesList_json)
            total = DataUtils.countSaleListPrice(salesList.get("count"), salesList.get("unitPrice"))
            allSaleListTotal.append(total)
        return sum(allSaleListTotal)

    @classmethod
    def getTotalOfPayAmount(cls, queryAll):
        allCustomPaymentInfo = []
        for item in queryAll:
            customPaymentInfo_json = json.dumps(object2dict(item), cls=DateEncoder)
            customPaymentInfo = json.loads(customPaymentInfo_json)
            total = DataUtils.strNumToDeciaml(customPaymentInfo.get("payAmount"))
            allCustomPaymentInfo.append(total)
        return sum(allCustomPaymentInfo)

    @classmethod
    def getTotalOfPurchase(cls, queryAll):
        allPurchase = []
        for item in queryAll:
            materialPurchase_json = json.dumps(object2dict(item), cls=DateEncoder)
            materialPurchase = json.loads(materialPurchase_json)
            total = DataUtils.strNumToDeciaml(materialPurchase.get("count"))
            allPurchase.append(total)
        return sum(allPurchase)


    @classmethod
    def getTotalOfWastage(cls, queryAll):
        allWastage = []
        for item in queryAll:
            wastagee_json = json.dumps(object2dict(item), cls=DateEncoder)
            wastage = json.loads(wastagee_json)
            total = DataUtils.strNumToDeciaml(wastage.get("wastageCount"))
            allWastage.append(total)
        return sum(allWastage)

    @classmethod
    def computeWastageRatio(cls, allWastage, allPurchase):
        wastageTotal = DataUtils.strNumToDeciaml(allWastage)
        purchaseTotal = DataUtils.strNumToDeciaml(allPurchase)
        ratio = wastageTotal/purchaseTotal
        return format(DataUtils.switchToPercent(ratio), '.2%')

    @classmethod
    def getSaleCount(cls, queryAll):
        allSaleCount = []
        for item in queryAll:
            allSaleCount.append(float(item.count))

        return sum(allSaleCount)


    @classmethod
    def getPurchaseCount(cls, queryAll):
        allPurchaseCount = []
        for item in queryAll:
            allPurchaseCount.append(float(item.count))

        return sum(allPurchaseCount)

    @classmethod
    def getAmountCount(cls, queryAll):
        allAmountCount = []
        for item in queryAll:
            itemAmount = float(item.count) * float(item.unitPrice)
            allAmountCount.append(itemAmount)

        return sum(allAmountCount)

    @classmethod
    def getMonthWastageCount(cls, queryAll):
        allMonthWastage = []
        for item in queryAll:
            allMonthWastage.append(float(item.wastageCount))

        return sum(allMonthWastage)


    @classmethod
    def getHomePageSummary(cls):
        session = DBSession()
        # 当年销售总量/总额
        queryAllCurrentYearSaleCount = session.query(SalesList).filter(
            SalesList.orderDate.like(DateUtils.get_current_Y()+"%")).all()
        currentYearSaleSum = BusinessViewUtils.getSaleCount(queryAllCurrentYearSaleCount)


        # 本月销售总量/总额
        queryAllCurrentMonthSaleCount = session.query(SalesList).filter(
            SalesList.orderDate.like(DateUtils.get_current_YM() + "%")).all()
        currentMonthSaleSum = BusinessViewUtils.getSaleCount(queryAllCurrentMonthSaleCount)
        currentMonthSaleAmount = BusinessViewUtils.getAmountCount(queryAllCurrentMonthSaleCount)

        # 上月销售总量/总额
        queryAllLastMonthSaleCount = session.query(SalesList).filter(
            SalesList.orderDate.like(DateUtils.get_last_YM() + "%")).all()
        lastMonthSaleSum = BusinessViewUtils.getSaleCount(queryAllLastMonthSaleCount)
        lastMonthSaleAmount = BusinessViewUtils.getAmountCount(queryAllLastMonthSaleCount)

        # 当年采购总量/总额
        queryAllCurrentYearPurchaseCount = session.query(MaterialPurchase).filter(
            MaterialPurchase.orderDate.like(DateUtils.get_current_Y() + "%")).all()
        currentYearPurchaseSum = BusinessViewUtils.getPurchaseCount(queryAllCurrentYearPurchaseCount)

        # 本月采购总量/总额
        queryAllCurrentMonthPurchaseCount = session.query(MaterialPurchase).filter(
            MaterialPurchase.orderDate.like(DateUtils.get_current_YM() + "%")).all()
        currentMonthPurchaseSum = BusinessViewUtils.getPurchaseCount(queryAllCurrentMonthPurchaseCount)
        currentMonthPurchaseAmount = BusinessViewUtils.getAmountCount(queryAllCurrentMonthPurchaseCount)

        # 上月采购总量/总额
        queryAllLastMonthPurchaseCount = session.query(MaterialPurchase).filter(
            MaterialPurchase.orderDate.like(DateUtils.get_last_YM() + "%")).all()
        lastMonthPurchaseSum = BusinessViewUtils.getPurchaseCount(queryAllLastMonthPurchaseCount)
        lastMonthPurchaseAmount = BusinessViewUtils.getAmountCount(queryAllLastMonthPurchaseCount)

        # 当年损耗总量
        queryAllCurrentYearWastage = session.query(WastageManage).filter(
            WastageManage.checkDate.like(DateUtils.get_current_Y()+"%")).all()
        currentYearWastageSum = BusinessViewUtils.getMonthWastageCount(queryAllCurrentYearWastage)

        # 当月损耗总量
        queryAllCurrentMonthWastage = session.query(WastageManage).filter(
            WastageManage.checkDate.like(DateUtils.get_current_YM()+"%")).all()
        currentMonthWastageSum = BusinessViewUtils.getMonthWastageCount(queryAllCurrentMonthWastage)

        # 上月损耗总量
        queryAllLastMonthWastage = session.query(WastageManage).filter(
            WastageManage.checkDate.like(DateUtils.get_last_YM()+"%")).all()
        lastMonthWastageSum = BusinessViewUtils.getMonthWastageCount(queryAllLastMonthWastage)


        session.close()

        return {"currentYearSaleSum": currentYearSaleSum,
                "currentMonthSaleSum": currentMonthSaleSum,
                "currentMonthSaleAmount": round(currentMonthSaleAmount, 2),
                "lastMonthSaleSum": lastMonthSaleSum,
                "lastMonthSaleAmount": round(lastMonthSaleAmount, 2),
                "currentYearPurchaseSum": currentYearPurchaseSum,
                "currentMonthPurchaseSum": currentMonthPurchaseSum,
                "currentMonthPurchaseAmount": round(currentMonthPurchaseAmount, 2),
                "lastMonthPurchaseSum": lastMonthPurchaseSum,
                "lastMonthPurchaseAmount": round(lastMonthPurchaseAmount, 2),
                "currentYearWastageSum": currentYearWastageSum,
                "currentMonthWastageSum": currentMonthWastageSum,
                "lastMonthWastageSum": lastMonthWastageSum
                }
