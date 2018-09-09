#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from django.db import models
from apps.BaseModels.models import CustomerManage,TractorManage,TrailerManage,StaffManage,UserManage,GasManage,Supplier
import apps.BaseModels.models

# Create your models here.




# class TestModle(models.Model):
#     testFiled = models.CharField(max_length=100, default="1")
#     testFiled2 = models.CharField(max_length=100, default="1")

# materialPurchase 【采购单表】
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


class MaterialPurchase(models.Model):
    purchaseID = models.CharField(max_length=100)
    supplierName = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    tractorID = models.CharField(max_length=100)
    trailerID = models.CharField(max_length=100)
    driverName = models.CharField(max_length=100)
    supercargo = models.CharField(max_length=100)
    count = models.CharField(max_length=100)
    unitPrice = models.CharField(max_length=100)
    mileage = models.CharField(max_length=100)
    orderDate = models.DateField()
    storageDate = models.DateField()
    isStoraged = models.CharField(max_length=100)

# salesList【销售单】
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


class SalesList(models.Model):
    salesListID = models.CharField(max_length=100)
    customName = models.CharField(max_length=100)
    customID = models.CharField(max_length=100)
    purchaseID = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    tractorID = models.CharField(max_length=100)
    trailerID = models.CharField(max_length=100)
    driverName = models.CharField(max_length=100)
    supercargo = models.CharField(max_length=100)
    count = models.CharField(max_length=100)
    unitPrice = models.CharField(max_length=100)
    mileage = models.CharField(max_length=100)
    orderDate = models.DateField()
    storageDate = models.DateField()
    comment = models.CharField(max_length=100)
    isInvoiced = models.CharField(max_length=100)
    isStoraged = models.CharField(max_length=100)
    # salesListID = models.CharField(max_length=100)
    # custom = models.ForeignKey(CustomerManage, on_delete=models.CASCADE,default='')
    # purchaseID = models.ForeignKey(MaterialPurchase, default='',on_delete=models.CASCADE)
    # #category = models.ForeignKey(GasManage,on_delete=models.CASCADE,default='')
    # tractor = models.ForeignKey(TractorManage, on_delete=models.CASCADE,default='')
    # trailer = models.ForeignKey(TrailerManage, on_delete=models.CASCADE,default='')
    # @property
    # def customID(self):
    #     return self.custom.customID




# vehicleMaintenanceManage【车辆维修安排（统计）】
# 类型（拖车/挂车）		vehicleType
# 拖车号/挂车号		vehicleID
# 维修时间		maintenanceDate
# 维修项目		maintenanceItems
# 费用		maintenanceCost
# 备注		maintenanceComment


class VehicleMaintenanceManage(models.Model):
    salesListID = models.CharField(max_length=100)
    vehicleType = models.CharField(max_length=100)
    vehicleID = models.CharField(max_length=100)
    maintenanceDate = models.DateField()
    maintenanceItems = models.CharField(max_length=100)
    maintenanceCost = models.CharField(max_length=100)
    maintenanceComment = models.CharField(max_length=100)
    wastageManage = models.CharField(max_length=100)
    trailerID = models.CharField(max_length=100)
    wastageCount = models.CharField(max_length=100)




# wastageManage【损耗校验】
# 挂车号		trailerID
# 损耗量 （吨）	默认值为现余量	wastageCount


class WastageManage(models.Model):
    trailerID = models.CharField(max_length=100)
    wastageCount = models.CharField(max_length=100)


# customPaymentInfo[客户充值信息]
# 客户名		customName
# 缴费时间		payTime
# 缴费金额		payAmount
# 余额 【计算出来的， 不能改】		balance


class CustomPaymentInfo(models.Model):
    customName = models.CharField(max_length=100)
    payTime = models.DateField()
    payAmount = models.CharField(max_length=100)
    balance = models.CharField(max_length=100)








