#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---------------------------------------------
    File  Name : BusinessUtils.py
    Author : agony
    Date : 2018/9/15
    Description: 
---------------------------------------------
"""
import json
from apps.BaseModels.BaseModelsORM.BaseORMViews import CustomerManageDBUtils, SupplierDBUtils, GasManageDBUtils,TrailerManageDBUtils, TractorManageDBUtils, StaffManageDBUtils
from apps.BussinessModels.BussinessModelsORM.BusinessORMViews import SalesListDBUtils,MaterialPurchaseDBUtils
from apps.AppUtils import DateUtils

class ViewModelsDBUtils(object):

    # 生成销售单编号(日期时间+6位流水index)
    @classmethod
    def generated_serial_number_for_salelist(cls):
        int_count_salelist = SalesListDBUtils.getCount() + 1
        str_count_salelist = str(int_count_salelist)
        return DateUtils.get_current_time() + str_count_salelist.zfill(6)

    # 生成采购单编号(日期时间+6位流水index)
    @classmethod
    def generated_serial_number_for_material_purchase(cls):
        int_count_salelist = MaterialPurchaseDBUtils.getCount() + 1
        str_count_salelist = str(int_count_salelist)
        return DateUtils.get_current_time() + str_count_salelist.zfill(6)

    # 查询所有客户名称
    @classmethod
    def getAllCustomNames(cls):
        allCustom = CustomerManageDBUtils.queryAll()
        allCustomNames = []
        if allCustom:
            for custom in allCustom:
                allCustomNames.append(custom['customName'])

        return json.dumps(allCustomNames)

    # 查询所有客户编号
    @classmethod
    def getAllCustomIDs(cls):
        allCustom = CustomerManageDBUtils.queryAll()
        allCustomIDs = []
        if allCustom:
            for custom in allCustom:
                allCustomIDs.append(custom['customID'])

        return json.dumps(allCustomIDs)

    # 查询所有供货商名称
    @classmethod
    def getAllSupplierNames(cls):
        allSupplier = SupplierDBUtils.queryAll()
        allSupplierNames = []
        if allSupplier:
            for supplier in allSupplier:
                allSupplierNames.append(supplier['supplierName'])

        return json.dumps(allSupplierNames)

    # 查询所有品种（气体种类）名称
    @classmethod
    def getAllGasName(cls):
        allGas = GasManageDBUtils.queryAll()
        allGasNames = []
        if allGas:
            for gas in allGas:
                allGasNames.append(gas['gasName'])

        return json.dumps(allGasNames)

    # 查询所有拖车的拖车号
    @classmethod
    def getAllTractorIDs(cls):
        allTractor = TractorManageDBUtils.queryAll()
        allTractorIDs = []
        if allTractor:
            for tractor in allTractor:
                allTractorIDs.append(tractor['tractorID'])

        return json.dumps(allTractorIDs)

    # 查询所有挂车的挂车号
    @classmethod
    def getTrailerIDs(cls):
        allTrailer = TrailerManageDBUtils.queryAll()
        allTrailerIDs = []
        if allTrailer:
            for trailer in allTrailer:
                allTrailerIDs.append(trailer['trailerID'])

        return json.dumps(allTrailerIDs)

    # 根据人员category查询所有人员name
    @classmethod
    def getAllStaffNamesByCategory(cls, category):
        allStaff = StaffManageDBUtils.queryAllByCategory(category)
        allStaffNames = []
        if allStaff:
            for staff in allStaff:
                allStaffNames.append(str(staff['staffName']))

        return allStaffNames

    # 查询所有司机名称
    @classmethod
    def getAllDriverNames(cls):
        return ViewModelsDBUtils.getAllStaffNamesByCategory(StaffManageDBUtils.STAFF_CATEGORY_DRIVER)

    # 查询所有押运员名称
    @classmethod
    def getAllSupercargoNames(cls):
        return ViewModelsDBUtils.getAllStaffNamesByCategory(StaffManageDBUtils.STAFF_CATEGORY_SUPERCARGO)








