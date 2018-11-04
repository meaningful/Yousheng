from django.shortcuts import render
from apps.AppUtils import EncodeUtils, LoginUtils
import json
from apps.BaseModels.BaseModelsORM.BaseORMViews import StaffManage, GasManage, CustomerManage, TrailerManage, Supplier, \
    TractorManage, User
from apps.BaseModels.BaseModelsORM.BaseORMViews import StaffManageDBUtils, GasManageDBUtils, CustomerManageDBUtils, \
    TrailerManageDBUtils, SupplierDBUtils, TractorManageDBUtils, UserDBUtils
from apps.BussinessModels.BussinessModelsORM.BusinessORMViews import SalesList, MaterialPurchase, \
    VehicleMaintenanceManage, WastageManage, CustomPaymentInfo
from apps.BussinessModels.BussinessModelsORM.BusinessORMViews import SalesListDBUtils, MaterialPurchaseDBUtils, \
    VehicleMaintenanceManageDBUtils, WastageManageDBUtils, CustomPaymentInfoDBUtils
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from apps.BusinessUtils import ViewModelsDBUtils, SelectItemDataUtils


def index(request):
    if request.method == 'GET':
        return render(request, "login.html")
    elif request.method == 'POST':
        userName = request.POST.get('userName')
        userPassword = request.POST.get('userPassword')
        user = LoginUtils.doLogin(userName, userPassword)
        if user:
            request.session["user_name"] = userName
            userLevel = user.userLevel
            request.session["user_level"] = userLevel
            context = {
                'userName': userName,
                'userLevel': userLevel
            }
            return render(request, "index.html", context=context)
        else:
            return render(request, "login.html", context={'error': '用户名或密码不正确!'})


def homePage(request):
    return render(request, "homePage.html")


def unfound(request):
    return render(request, "404.html")


def carfixManage(request):
    return render(request, "carfixManage.html")


# 公司人员管理
def staffManage(request):
    allStaffs = StaffManageDBUtils.queryAll()
    return render(request, "staffManage.html", {'showData': json.dumps(allStaffs)})


# 气体管理
def gasManage(request):
    allGas = GasManageDBUtils.queryAll()
    return render(request, "gasManage.html", {'showData': json.dumps(allGas)})


# 客户管理
def customManage(request):
    allCustom = CustomerManageDBUtils.queryAll()
    return render(request, "customManage.html", {'showData': json.dumps(allCustom)})


# 挂车管理
def trailerManage(request):
    allTrailer = TrailerManageDBUtils.queryAll()
    return render(request, "trailerManage.html", {'showData': json.dumps(allTrailer)})


# 拖车管理
def tractorManage(request):
    allTractor = TractorManageDBUtils.queryAll()
    return render(request, "tractorManage.html", {'showData': json.dumps(allTractor)})


# 供应商管理
def supplier(request):
    allSupplier = SupplierDBUtils.queryAll()
    return render(request, "supplier.html", {'showData': json.dumps(allSupplier)})


# 销售单
def salesList(request):
    allSalesList = SalesListDBUtils.queryAllSalesListByIsStoraged(SalesListDBUtils.IS_STORAGED_NO)
    return render(request, "salesList.html", {'showData': json.dumps(allSalesList)})


# 采购单
def materialPurchase(request):
    allmaterialPurchase = MaterialPurchaseDBUtils.queryAllMaterialPurchaseByIsStoraged(
        MaterialPurchaseDBUtils.IS_STORAGED_NO)
    return render(request, "materialPurchase.html", {'showData': json.dumps(allmaterialPurchase)})


# 车辆维修安排(统计)
def vehicleMaintenanceManage(request):
    allVehicleMaintenanceManage = VehicleMaintenanceManageDBUtils.queryAll()
    return render(request, "vehicleMaintenanceManage.html", {'showData': json.dumps(allVehicleMaintenanceManage)})


# 损耗校验
def wastageManage(request):
    allWastageManage = WastageManageDBUtils.queryAll()
    return render(request, "wastageManage.html", {'showData': json.dumps(allWastageManage)})


# 客户充值信息
def customPaymentInfo(request):
    allCustomPaymentInfo = CustomPaymentInfoDBUtils.queryAll()
    return render(request, "customPaymentInfo.html", {'showData': json.dumps(allCustomPaymentInfo)})


# 客户余额信息
def customBalanceInfo(request):
    allCustomPaymentInfo = CustomPaymentInfoDBUtils.queryAll()
    return render(request, "customBalanceInfo.html", {'showData': json.dumps(allCustomPaymentInfo)})


# 用户管理
def userManage(request):
    allUsers = UserDBUtils.queryAll()
    return render(request, "userManage.html", {'showData': json.dumps(allUsers)})


# 客户对账单
def customerBillList(request):
    return render(request, "customerBillList.html")


def customerStatement(request):
    return render(request, "customerStatement.html")


# 查询客户对账单数据
def searchForCustomerBillList(request):
    customName = request.GET.get("customName")
    fromDate = request.GET.get("fromDate")
    deadline = request.GET.get("deadline")
    allSalesList = SalesListDBUtils.queryAllSalesListForCustomerBillList(customName, fromDate, deadline)
    return JsonResponse({'showData': json.dumps(allSalesList)})


def searchCustomerBalanceInfo(request):
    customName = request.GET.get("customName")
    allCustomBalanceInfo = CustomPaymentInfoDBUtils.queryAllLatestByCustomName(customName)
    return JsonResponse({'showData': json.dumps(allCustomBalanceInfo)})


# 销售报表
def salesListReport(request):
    return render(request, "salesListReport.html")


# 根据时间段查询已入库的销售单
def searchSalesListByDate(request):
    fromDate = request.GET.get("fromDate")
    deadline = request.GET.get("deadline")
    # invoiced = request.GET.get("invoiced")
    # isInvoiced = ""
    # if invoiced == SalesListDBUtils.IS_INVOICED_YES:
    #     isInvoiced = SalesListDBUtils.IS_INVOICED_YES
    # elif invoiced == SalesListDBUtils.IS_INVOICED_NO:
    #     isInvoiced = SalesListDBUtils.IS_INVOICED_NO
    # else:
    #     isInvoiced = SalesListDBUtils.IS_INVOICED_NA

    allSalesList = SalesListDBUtils.queryAllSalesListByDate(fromDate, deadline)
    return JsonResponse({'showData': json.dumps(allSalesList)})


# 采购报表
def materialPurchaseReport(request):
    return render(request, "materialPurchaseReport.html")


# 根据时间段查询已入库的采购单
def searchMaterialPurchaseByDate(request):
    fromDate = request.GET.get("fromDate")
    deadline = request.GET.get("deadline")
    allMaterialPurchase = MaterialPurchaseDBUtils.queryAllMaterialPurchaseByDate(
        MaterialPurchaseDBUtils.IS_STORAGED_YES, fromDate, deadline)
    return JsonResponse({'showData': json.dumps(allMaterialPurchase)})


# 月损耗列表
def monthWastage(request):
    return render(request, "monthWastage.html")

# 损耗查询
def searchMonthWastage(request):
    trailerID = request.GET.get("trailerID")
    fromDate = request.GET.get("fromDate")
    deadline = request.GET.get("deadline")

    allMonthWastage = WastageManageDBUtils.queryMonthWastage(trailerID, fromDate, deadline)
    return JsonResponse({'showData': json.dumps(allMonthWastage)})


# 维修查询
def searchMaintenanceByType(request):
    maintainType = request.GET.get("maintainType")


    if VehicleMaintenanceManageDBUtils.MAINTAIN_TYPE_ALL == maintainType:
        allMaintenance = VehicleMaintenanceManageDBUtils.queryAll()
    else:
        allMaintenance = VehicleMaintenanceManageDBUtils.queryMaintenanceByType(maintainType)

    return JsonResponse({'showData': json.dumps(allMaintenance)})


@csrf_exempt
def editCustomManage(request):
    mode = request.POST.get('oper')

    editId = request.POST.get('id')
    customID = request.POST.get('customID')
    customName = request.POST.get('customName')
    tel = request.POST.get('tel')
    addr = request.POST.get('addr')
    taxFileNO = request.POST.get('taxFileNO')
    bankOfDepsit = request.POST.get('bankOfDepsit')
    bankAccount = request.POST.get('bankAccount')
    fax = request.POST.get('fax')
    industryField = request.POST.get('industryField')
    companyNature = request.POST.get('companyNature')
    consocationMode = request.POST.get('consocationMode')
    level = request.POST.get('level')
    contract = request.POST.get('contract')
    payCycle = request.POST.get('payCycle')
    companyCharge = request.POST.get('companyCharge')
    companyContact = request.POST.get('companyContact')
    customQualification = request.POST.get('customQualification')
    annualSales = request.POST.get('annualSales')

    custom = CustomerManage(customID=customID, customName=customName, tel=tel, addr=addr, taxFileNO=taxFileNO,
                            bankOfDepsit=bankOfDepsit, bankAccount=bankAccount, fax=fax,
                            industryField=industryField, companyNature=companyNature, consocationMode=consocationMode,
                            level=level, contract=contract, payCycle=payCycle,
                            companyCharge=companyCharge, companyContact=companyContact,
                            customQualification=customQualification, annualSales=annualSales)

    if mode == 'add':
        newID = CustomerManageDBUtils.add(custom)
        return JsonResponse({'new_id': newID})

    if mode == 'del' and editId:
        CustomerManageDBUtils.delete(editId)
        return HttpResponse("OK")

    if mode == 'edit' and editId:
        CustomerManageDBUtils.update(editId, custom)
        return HttpResponse("OK")


@csrf_exempt
def editStaffManage(request):
    mode = request.POST.get('oper')

    editId = request.POST.get('id')
    staffID = request.POST.get('staffID')
    staffName = request.POST.get('staffName')
    idNumber = request.POST.get('idNumber')
    hiredate = request.POST.get('hiredate')
    position = request.POST.get('position')
    photo = request.POST.get('photo')
    resume = request.POST.get('resume')
    category = request.POST.get('category')

    staff = StaffManage(staffID=staffID, staffName=staffName, idNumber=idNumber, hiredate=hiredate,
                        position=position, photo=photo, resume=resume, category=category)

    if mode == 'add':
        newID = StaffManageDBUtils.add(staff)
        return JsonResponse({'new_id': newID})

    if mode == 'del' and editId:
        StaffManageDBUtils.delete(editId)
        return HttpResponse("OK")

    if mode == 'edit' and editId:
        StaffManageDBUtils.update(editId, staff)
        return HttpResponse("OK")


@csrf_exempt
def editGasManage(request):
    mode = request.POST.get('oper')

    editId = request.POST.get('id')
    gasID = request.POST.get('gasID')
    gasName = request.POST.get('gasName')

    gas = GasManage(gasID=gasID, gasName=gasName)

    if mode == 'add':
        newID = GasManageDBUtils.add(gas)
        return JsonResponse({'new_id': newID})

    if mode == 'del' and editId:
        GasManageDBUtils.delete(editId)
        return HttpResponse("OK")

    if mode == 'edit' and editId:
        GasManageDBUtils.update(editId, gas)
        return HttpResponse("OK")


@csrf_exempt
def editTrailerManage(request):
    mode = request.POST.get('oper')

    editId = request.POST.get('id')
    trailerID = request.POST.get('trailerID')
    annualInspectionTime = request.POST.get('annualInspectionTime')
    annualInspectionCycle = request.POST.get('annualInspectionCycle')
    insuranceTime = request.POST.get('insuranceTime')
    chassisNumber = request.POST.get('chassisNumber')
    deliveryTime = request.POST.get('deliveryTime')
    currentBalance = request.POST.get('currentBalance')

    trailer = TrailerManage(trailerID=trailerID, annualInspectionTime=annualInspectionTime,
                            annualInspectionCycle=annualInspectionCycle, insuranceTime=insuranceTime,
                            chassisNumber=chassisNumber, deliveryTime=deliveryTime, currentBalance=currentBalance)

    if mode == 'add':
        newID = TrailerManageDBUtils.add(trailer)
        return JsonResponse({'new_id': newID})

    if mode == 'del' and editId:
        TrailerManageDBUtils.delete(editId)
        return HttpResponse("OK")

    if mode == 'edit' and editId:
        TrailerManageDBUtils.update(editId, trailer)
        return HttpResponse("OK")


@csrf_exempt
def editTractorManage(request):
    mode = request.POST.get('oper')

    editId = request.POST.get('id')
    tractorID = request.POST.get('tractorID')
    annualInspectionTime = request.POST.get('annualInspectionTime')
    annualInspectionCycle = request.POST.get('annualInspectionCycle')
    insuranceTime = request.POST.get('insuranceTime')
    chassisNumber = request.POST.get('chassisNumber')
    deliveryTime = request.POST.get('deliveryTime')
    initMileage = request.POST.get('initMileage')

    tractor = TractorManage(tractorID=tractorID, annualInspectionTime=annualInspectionTime,
                            annualInspectionCycle=annualInspectionCycle, insuranceTime=insuranceTime,
                            chassisNumber=chassisNumber, deliveryTime=deliveryTime, initMileage=initMileage)

    if mode == 'add':
        newID = TractorManageDBUtils.add(tractor)
        return JsonResponse({'new_id': newID})

    if mode == 'del' and editId:
        TractorManageDBUtils.delete(editId)
        return HttpResponse("OK")

    if mode == 'edit' and editId:
        TractorManageDBUtils.update(editId, tractor)
        return HttpResponse("OK")


@csrf_exempt
def editSupplier(request):
    mode = request.POST.get('oper')

    editId = request.POST.get('id')
    supplierID = request.POST.get('supplierID')
    supplierName = request.POST.get('supplierName')
    tel = request.POST.get('tel')
    addr = request.POST.get('addr')
    companyChargeName = request.POST.get('companyChargeName')
    companyChargePosition = request.POST.get('companyChargePosition')
    companyChargeTel = request.POST.get('companyChargeTel')
    companyContactName = request.POST.get('companyContactName')
    companyContactPosition = request.POST.get('companyContactPosition')
    companyContactTel = request.POST.get('companyContactTel')
    customQualification = request.POST.get('customQualification')
    customTaxFileNO = request.POST.get('customTaxFileNO')
    customBankOfDepsit = request.POST.get('customBankOfDepsit')
    customBankAccount = request.POST.get('customBankAccount')
    customContactName = request.POST.get('customContactName')
    customContactTel = request.POST.get('customContactTel')
    purchaseCategory = request.POST.get('purchaseCategory')

    supplier = Supplier(supplierID=supplierID, supplierName=supplierName, tel=tel, addr=addr,
                        companyChargeName=companyChargeName, companyChargePosition=companyChargePosition,
                        companyChargeTel=companyChargeTel, companyContactName=companyContactName,
                        companyContactPosition=companyContactPosition, companyContactTel=companyContactTel,
                        customQualification=customQualification, customTaxFileNO=customTaxFileNO,
                        customBankOfDepsit=customBankOfDepsit, customBankAccount=customBankAccount,
                        customContactName=customContactName, customContactTel=customContactTel,
                        purchaseCategory=purchaseCategory)

    if mode == 'add':
        newID = SupplierDBUtils.add(supplier)
        return JsonResponse({'new_id': newID})

    if mode == 'del' and editId:
        SupplierDBUtils.delete(editId)
        return HttpResponse("OK")

    if mode == 'edit' and editId:
        SupplierDBUtils.update(editId, supplier)
        return HttpResponse("OK")


@csrf_exempt
def editSalesList(request):
    mode = request.POST.get('oper')

    editId = request.POST.get('id')
    # salesListID = request.POST.get('salesListID')
    customName = request.POST.get('customName')
    customID = request.POST.get('customID')
    purchaseID = "NA"
    category = request.POST.get('category')
    tractorID = request.POST.get('tractorID')
    trailerID = request.POST.get('trailerID')
    driverName = request.POST.get('driverName')
    supercargo = request.POST.get('supercargo')
    count = request.POST.get('count')
    unitPrice = request.POST.get('unitPrice')
    mileage = request.POST.get('mileage')
    orderDate = request.POST.get('orderDate')
    storageDate = request.POST.get('storageDate')
    comment = request.POST.get('comment')
    isInvoiced = "NA"
    isStoraged = request.POST.get('isStoraged')

    if mode == 'add':
        salesListID = ViewModelsDBUtils.generated_serial_number_for_salelist()
        salesList = SalesList(salesListID=salesListID, customName=customName, customID=customID,
                              purchaseID=purchaseID, category=category, tractorID=tractorID, trailerID=trailerID,
                              driverName=driverName, supercargo=supercargo, count=count, unitPrice=unitPrice,
                              mileage=mileage, orderDate=orderDate, storageDate=storageDate, comment=comment,
                              isInvoiced=isInvoiced, isStoraged=isStoraged)

        newID = SalesListDBUtils.add(salesList)
        return JsonResponse({'new_id': newID})

    if mode == 'del' and editId:
        SalesListDBUtils.delete(editId)
        return HttpResponse("OK")

    if mode == 'edit' and editId:
        salesListID = SalesListDBUtils.getSalesListIDByEditId(editId)
        salesList = SalesList(salesListID=salesListID, customName=customName, customID=customID,
                              purchaseID=purchaseID, category=category, tractorID=tractorID, trailerID=trailerID,
                              driverName=driverName, supercargo=supercargo, count=count, unitPrice=unitPrice,
                              mileage=mileage, orderDate=orderDate, storageDate=storageDate, comment=comment,
                              isInvoiced=isInvoiced, isStoraged=isStoraged)
        SalesListDBUtils.update(editId, salesList)
        return HttpResponse("OK")


@csrf_exempt
def editMaterialPurchaseManage(request):
    mode = request.POST.get('oper')

    editId = request.POST.get('id')
    # purchaseID = request.POST.get('purchaseID')
    supplierName = request.POST.get('supplierName')
    category = request.POST.get('category')
    tractorID = request.POST.get('tractorID')
    trailerID = request.POST.get('trailerID')
    driverName = request.POST.get('driverName')
    supercargo = request.POST.get('supercargo')
    count = request.POST.get('count')
    unitPrice = request.POST.get('unitPrice')
    mileage = request.POST.get('mileage')
    orderDate = request.POST.get('orderDate')
    storageDate = request.POST.get('storageDate')
    isStoraged = request.POST.get('isStoraged')

    if mode == 'add':
        # 采购单编号后台生成，不可编辑，保证唯一性
        # Add 时创建编号
        purchaseID = ViewModelsDBUtils.generated_serial_number_for_material_purchase()
        materialPurchase = MaterialPurchase(purchaseID=purchaseID, supplierName=supplierName,
                                            category=category, tractorID=tractorID,
                                            trailerID=trailerID, driverName=driverName,
                                            supercargo=supercargo, count=count,
                                            unitPrice=unitPrice, mileage=mileage, orderDate=orderDate,
                                            storageDate=storageDate, isStoraged=isStoraged)
        newID = MaterialPurchaseDBUtils.add(materialPurchase)
        return JsonResponse({'new_id': newID})

    if mode == 'del' and editId:
        MaterialPurchaseDBUtils.delete(editId)
        return HttpResponse("OK")

    if mode == 'edit' and editId:
        # 采购单编号后台生成，不可编辑，保证唯一性
        # Update 时根据 editId 查询编号
        purchaseID = MaterialPurchaseDBUtils.getPurchaseIDByEditId(editId)
        materialPurchase = MaterialPurchase(purchaseID=purchaseID, supplierName=supplierName,
                                            category=category, tractorID=tractorID,
                                            trailerID=trailerID, driverName=driverName,
                                            supercargo=supercargo, count=count,
                                            unitPrice=unitPrice, mileage=mileage, orderDate=orderDate,
                                            storageDate=storageDate, isStoraged=isStoraged)
        MaterialPurchaseDBUtils.update(editId, materialPurchase)
        return HttpResponse("OK")


@csrf_exempt
def editVehicleMaintenanceManage(request):
    mode = request.POST.get('oper')

    editId = request.POST.get('id')
    vehicleType = request.POST.get('vehicleType')
    vehicleID = request.POST.get('vehicleID')
    maintenanceDate = request.POST.get('maintenanceDate')
    maintainType = request.POST.get('maintainType')
    maintenanceItems = request.POST.get('maintenanceItems')
    maintenanceCost = request.POST.get('maintenanceCost')
    maintenanceComment = request.POST.get('maintenanceComment')

    vehicleMaintenanceManage = VehicleMaintenanceManage(vehicleType=vehicleType, vehicleID=vehicleID,
                                                        maintenanceDate=maintenanceDate,
                                                        maintainType=maintainType,
                                                        maintenanceItems=maintenanceItems,
                                                        maintenanceCost=maintenanceCost,
                                                        maintenanceComment=maintenanceComment)

    if mode == 'add':
        newID = VehicleMaintenanceManageDBUtils.add(vehicleMaintenanceManage)
        return JsonResponse({'new_id': newID})

    if mode == 'del' and editId:
        VehicleMaintenanceManageDBUtils.delete(editId)
        return HttpResponse("OK")

    if mode == 'edit' and editId:
        VehicleMaintenanceManageDBUtils.update(editId, vehicleMaintenanceManage)
        return HttpResponse("OK")


@csrf_exempt
def editWastageManage(request):
    mode = request.POST.get('oper')

    editId = request.POST.get('id')
    trailerID = request.POST.get('trailerID')
    wastageCount = request.POST.get('wastageCount')
    checkDate = request.POST.get('checkDate')
    wastageRatio = "NA"

    wastageManage = WastageManage(trailerID=trailerID, wastageCount=wastageCount, checkDate=checkDate,
                                  wastageRatio=wastageRatio)

    if mode == 'add':
        newID = WastageManageDBUtils.add(wastageManage)
        return JsonResponse({'new_id': newID})

    if mode == 'del' and editId:
        WastageManageDBUtils.delete(editId)
        return HttpResponse("OK")

    if mode == 'edit' and editId:
        WastageManageDBUtils.update(editId, wastageManage)
        return HttpResponse("OK")


@csrf_exempt
def editCustomPaymentInfo(request):
    mode = request.POST.get('oper')

    editId = request.POST.get('id')
    customName = request.POST.get('customName')
    payTime = request.POST.get('payTime')
    payAmount = request.POST.get('payAmount')
    # balance 为计算出来的值，所以这里是空，先用假数据
    balance = request.POST.get('balance')

    customPaymentInfo = CustomPaymentInfo(customName=customName, payTime=payTime, payAmount=payAmount, balance="0")

    if mode == 'add':
        newID = CustomPaymentInfoDBUtils.add(customPaymentInfo)
        return JsonResponse({'new_id': newID})

    if mode == 'del' and editId:
        CustomPaymentInfoDBUtils.delete(editId)
        return HttpResponse("OK")

    if mode == 'edit' and editId:
        CustomPaymentInfoDBUtils.update(editId, customPaymentInfo)
        return HttpResponse("OK")


@csrf_exempt
def editUser(request):
    mode = request.POST.get('oper')

    editId = request.POST.get('id')
    userName = request.POST.get('userName')
    userPassword = request.POST.get('userPassword')
    userLevel = request.POST.get('userLevel')

    user = User(userName=userName, userPassword=EncodeUtils.encode(userPassword), userLevel=userLevel)

    if mode == 'add':
        newID = UserDBUtils.add(user)
        return JsonResponse({'new_id': newID})

    if mode == 'del' and editId:
        UserDBUtils.delete(editId)
        return HttpResponse("OK")

    if mode == 'edit' and editId:
        UserDBUtils.update(editId, user)
        return HttpResponse("OK")


# 查询所有客户名称
@csrf_exempt
def getAllCustomNames(request):
    allCustomNames = SelectItemDataUtils.getAllCustomNames()
    return JsonResponse({"allCustomNames": allCustomNames})


#
#
# # 查询所有客户编号
# @csrf_exempt
# def getAllCustomIDs(request):
#     allCustomIDs = ViewModelsDBUtils.getAllCustomIDs()
#     return JsonResponse({"allCustomIDs": allCustomIDs})
#
#
# # 查询所有供货商名称
# @csrf_exempt
# def getAllSupplierNames(request):
#     allSupplierNames = ViewModelsDBUtils.getAllSupplierNames()
#     return JsonResponse({"allSupplierNames": allSupplierNames})


# 获取所有品种（气体种类）名称
@csrf_exempt
def getAllGasName(request):
    allGasNames = SelectItemDataUtils.getAllGasNames()
    return JsonResponse({"allGasNames": allGasNames})


# 生成销售单的编号
@csrf_exempt
def generatedSerialNumberForSaleList(request):
    serialNo = ViewModelsDBUtils.generated_serial_number_for_salelist()
    strOption = "<select> <option value=" + serialNo + ">" + serialNo + "</option> </select>"
    return HttpResponse(strOption)


# 生成采购单编号
@csrf_exempt
def generatedSerialNumberForMaterialPurchase(request):
    serialNo = ViewModelsDBUtils.generated_serial_number_for_material_purchase()
    strOption = "<select> <option value=" + serialNo + ">" + serialNo + "</option> </select>"
    return HttpResponse(strOption)


# # 查询所有拖车的拖车号
# @csrf_exempt
# def getAllTractorIDs(request):
#     allTractorIDs = ViewModelsDBUtils.getAllTractorIDs()
#     return JsonResponse({"allTractorIDs": allTractorIDs})


# 查询所有挂车号
@csrf_exempt
def getTrailerIDs(request):
    allTrailerIDs = SelectItemDataUtils.getAllTrailerIDs()
    return JsonResponse({"allTrailerIDs": allTrailerIDs})


# 查询所有挂车/拖车号
@csrf_exempt
def getAllVehicleIDs(request):
    allVehicleIDs = SelectItemDataUtils.getAllVehicleIDs()
    return JsonResponse({"allVehicleIDs": allVehicleIDs})


#
# # 查询所有司机名称
# @csrf_exempt
# def getAllDriverNames(request):
#     allDriverNames = ViewModelsDBUtils.getAllDriverNames()
#     return JsonResponse({"allDriverNames": allDriverNames})
#
#
# # 查询所有押运员名称
# @csrf_exempt
# def getAllSupercargoNames(request):
#     allSupercargoNames = ViewModelsDBUtils.getAllSupercargoNames()
#     return JsonResponse({"allSupercargoNames": allSupercargoNames})


# 获取客户对账单页面select选项数据
def getCustomerBillListSelectData(request):
    allSelectItemDatas = SelectItemDataUtils.getAllSelectItemDataForCustomerBillList()
    return JsonResponse({"allCustomNames": allSelectItemDatas["allCustomNames"],
                         "earliestStorageDate": allSelectItemDatas["earliestStorageDate"],
                         "latestStorageDate": allSelectItemDatas["latestStorageDate"]})


# 获取销售单 Select item 的数据
@csrf_exempt
def getAllSelectItemDataForSaleList(request):
    allSelectItemDatas = SelectItemDataUtils.getAllSelectItemDataForSaleList()
    return JsonResponse({"allCustomNames": allSelectItemDatas["allCustomNames"],
                         "allCustomIDs": allSelectItemDatas["allCustomIDs"],
                         "allGasNames": allSelectItemDatas["allGasNames"],
                         "allTractorIDs": allSelectItemDatas["allTractorIDs"],
                         "allTrailerIDs": allSelectItemDatas["allTrailerIDs"],
                         "allDriverNames": allSelectItemDatas["allDriverNames"],
                         "allSupercargoNames": allSelectItemDatas["allSupercargoNames"]})


# 获取采购单 Select item 的数据
@csrf_exempt
def getAllSelectItemDataForMaterialPurchase(request):
    serialNo = ViewModelsDBUtils.generated_serial_number_for_material_purchase()
    allSelectItemDatas = SelectItemDataUtils.getAllSelectItemDataForMaterialPurchase()

    return JsonResponse({"serialNo": serialNo,
                         "allSupplierNames": allSelectItemDatas["allSupplierNames"],
                         "allGasNames": allSelectItemDatas["allGasNames"],
                         "allTractorIDs": allSelectItemDatas["allTractorIDs"],
                         "allTrailerIDs": allSelectItemDatas["allTrailerIDs"],
                         "allDriverNames": allSelectItemDatas["allDriverNames"],
                         "allSupercargoNames": allSelectItemDatas["allSupercargoNames"]})
