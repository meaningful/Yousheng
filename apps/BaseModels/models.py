#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

# <- 客户管理表 Begin ->
# 客户编号		customID
# 名称	单位名称+简称	customName
# 电话		tel
# 地址		addr
# 税号		taxFileNO
# 开户行		bankOfDepsit
# 账号		bankAccount
# 传真		fax
# 所属行业		industryField
# 公司性质		companyNature
# 用气种类	【废弃，不用】	gasCategory
# 储罐大小	【废弃，不用】	gasTankSize
# 合作类型	【直供， 共建，中间站】	consocationMode
# 等级	【A/B/C/D】	level
# 合同	【varchar(256)】 合同号	contract
# 付款周期		payCycle
# 公司负责人		companyCharge
# 公司联系人		companyContact
# 客户资质	三证	customQualification
# 年销售额		annualSales


class CustomerManage(models.Model):
    customID = models.CharField(max_length=100)
    customName = models.CharField(max_length=100)
    tel = models.CharField(max_length=20)
    addr = models.CharField(max_length=100)
    taxFileNO = models.CharField(max_length=100)
    bankOfDepsit = models.CharField(max_length=100)
    bankAccount = models.CharField(max_length=100)
    fax = models.CharField(max_length=100)
    industryField = models.CharField(max_length=100)
    companyNature = models.CharField(max_length=100)
    consocationMode = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    contract = models.CharField(max_length=100)
    payCycle = models.DateField()
    companyCharge = models.CharField(max_length=100)
    companyContact = models.CharField(max_length=100)
    customQualification = models.CharField(max_length=100)
    annualSales = models.CharField(max_length=100)

    def __repr__(self):
        return repr((self.customID, self.customName, self.tel))

# <- 客户管理表 End ->


# <- 供货商管理表 Begin ->
# 供应商编号		supplierID
# 单位名称		supplierName
# 电话		tel
# 地址		addr
# 公司负责人（姓名）		companyChargeName
# 公司负责人（职务）		companyChargePosition
# 公司负责人（电话）		companyChargeTel
# 公司联系人（姓名）		companyContactName
# 公司联系人（职务）		companyContactPosition
# 公司联系人（电话）		companyContactTel
# 客户资质	三证	customQualification
# 客户资质（税号）		customTaxFileNO
# 客户资质（开户行）		customBankOfDepsit
# 客户资质（账号）		customBankAccount
# 客户资质（联系人）		customContactName
# 客户资质（手机）		customContactTel
# 采购品种		purchaseCategory


class Supplier(models.Model):
    supplierID = models.CharField(max_length=100)
    supplierName = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    addr = models.CharField(max_length=100)
    companyChargeName = models.CharField(max_length=100)
    companyChargePosition = models.CharField(max_length=100)
    companyChargeTel = models.CharField(max_length=100)
    companyContactName = models.CharField(max_length=100)
    companyContactPosition = models.CharField(max_length=100)
    companyContactTel = models.CharField(max_length=100)
    customQualification = models.CharField(max_length=100)
    customTaxFileNO = models.CharField(max_length=100)
    customBankOfDepsit = models.CharField(max_length=100)
    customBankAccount = models.CharField(max_length=100)
    customContactName = models.CharField(max_length=100)
    customContactTel = models.CharField(max_length=100)
    purchaseCategory = models.CharField(max_length=100)

# <- 供货商管理 End ->

# <- 气体管理表 Begin ->
# 气体编号		gasID
# 气体名称		gasName


class GasManage(models.Model):
    gasID = models.CharField(max_length=100)
    gasName = models.CharField(max_length=100)

# <- 气体管理表 End ->


# <- 拖车管理表 Begin ->
# 车牌号		tractorID
# 年检时间		annualInspectionTime
# 年检周期       annualInspectionCycle
# 保险时间		insuranceTime
# 车架号		chassisNumber
# 出厂时间		deliveryTime
# 初始码表数    initMileage


class TractorManage(models.Model):
    tractorID = models.CharField(max_length=100)
    annualInspectionTime = models.DateField()
    annualInspectionCycle = models.IntegerField()
    insuranceTime = models.DateField()
    chassisNumber = models.CharField(max_length=100)
    deliveryTime = models.CharField(max_length=100)
    initMileage = models.CharField(max_length=100)

# <- 拖车管理表 End ->


# <- 挂车管理表 Begin ->
# 挂车号		trailerID
# 年检时间		annualInspectionTime
# 年检周期       annualInspectionCycle
# 保险时间		insuranceTime
# 车架号		chassisNumber
# 出厂时间		deliveryTime
# 现余量 currentBalance （现余量=该挂车对应采购单数量之和 - 该挂车对应销售单数量之和 - 该挂车损耗校验之和）


class TrailerManage(models.Model):
    trailerID = models.CharField(max_length=100)
    annualInspectionTime = models.DateField()
    annualInspectionCycle = models.IntegerField()
    insuranceTime = models.DateField()
    chassisNumber = models.CharField(max_length=100)
    deliveryTime = models.CharField(max_length=100)
    currentBalance = models.CharField(max_length=100)

# <- 挂车管理表 End ->


# <- 公司人员管理表 Begin ->
# 编号		staffID
# 姓名		staffName
# 身份证号		idNumber
# 入职时间		hiredate
# 职务		position
# 照片		photo
# 人员简历		resume
# 人员类别	（办公室/司机/押运员）	category


class StaffManage(models.Model):
    staffID = models.CharField(max_length=100)
    staffName = models.CharField(max_length=100)
    idNumber = models.CharField(max_length=100)
    hiredate = models.DateField()
    position = models.CharField(max_length=100)
    photo = models.CharField(max_length=100)
    resume = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

# <- 公司人员管理表 End ->


# <- 用户管理表 Begin ->
# 用户名		userName
# 密码		userPassword
# 用户权限级别 userLevel


class UserManage(models.Model):
    userName = models.CharField(max_length=100)
    userPassword = models.CharField(max_length=256)
    userLevel = models.CharField(max_length=100)

# <- 用户管理表 End ->

