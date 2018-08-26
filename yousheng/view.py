from django.shortcuts import render
from apps.AppUtils import EncodeUtils, LoginUtils
import json
from apps.BaseModels.BaseModelsORM.BaseORMViews import StaffManage, GasManage, CustomerManage,TrailerManage, Supplier, TractorManage, User
from apps.BaseModels.BaseModelsORM.BaseORMViews import StaffManageDBUtils, GasManageDBUtils, CustomerManageDBUtils, TrailerManageDBUtils, SupplierDBUtils, TractorManageDBUtils, UserDBUtils
from apps.BussinessModels.BussinessModelsORM.BusinessORMViews import SalesList, MaterialPurchase, VehicleMaintenanceManage, WastageManage, CustomPaymentInfo
from apps.BussinessModels.BussinessModelsORM.BusinessORMViews import SalesListDBUtils, MaterialPurchaseDBUtils, VehicleMaintenanceManageDBUtils, WastageManageDBUtils, CustomPaymentInfoDBUtils
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponse


# def json_default(value):
#     if isinstance(value, datetime.date):
#         return dict(year=value.year, month=value.month, day=value.day)
#     else:
#         return value.__dict__

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
    return render(request, "customManage.html",  {'showData': json.dumps(allCustom)})


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
    allSalesList = SalesListDBUtils.queryAll()
    return render(request, "salesList.html", {'showData': json.dumps(allSalesList)})


# 采购单
def materialPurchase(request):
    allmaterialPurchase = MaterialPurchaseDBUtils.queryAll()
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


# 用户管理
def userManage(request):
    allUsers = UserDBUtils.queryAll()
    return render(request, "userManage.html", {'showData': json.dumps(allUsers)})


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
        CustomerManageDBUtils.add(custom)
        return HttpResponse("OK")

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
        StaffManageDBUtils.add(staff)
        return HttpResponse("OK")

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
        GasManageDBUtils.add(gas)
        return HttpResponse("OK")

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
    insuranceTime = request.POST.get('insuranceTime')
    chassisNumber = request.POST.get('chassisNumber')
    deliveryTime = request.POST.get('deliveryTime')

    trailer = TrailerManage(trailerID=trailerID, annualInspectionTime=annualInspectionTime, insuranceTime=insuranceTime,
                            chassisNumber=chassisNumber, deliveryTime=deliveryTime)

    if mode == 'add':
        TrailerManageDBUtils.add(trailer)
        return HttpResponse("OK")

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
    insuranceTime = request.POST.get('insuranceTime')
    chassisNumber = request.POST.get('chassisNumber')
    deliveryTime = request.POST.get('deliveryTime')

    tractor = TractorManage(tractorID=tractorID, annualInspectionTime=annualInspectionTime, insuranceTime=insuranceTime,
                            chassisNumber=chassisNumber, deliveryTime=deliveryTime)

    if mode == 'add':
        TractorManageDBUtils.add(tractor)
        return HttpResponse("OK")

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
        SupplierDBUtils.add(supplier)
        return HttpResponse("OK")

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
    salesListID = request.POST.get('salesListID')
    customName = request.POST.get('customName')
    customID = request.POST.get('customID')
    purchaseID = request.POST.get('purchaseID')
    category = request.POST.get('category')
    tractorID = request.POST.get('tractorID')
    trailerID = request.POST.get('trailerID')
    driverName = request.POST.get('driverName')
    supercargo = request.POST.get('supercargo')
    count = request.POST.get('count')
    unitPrice = request.POST.get('unitPrice')
    mileage = request.POST.get('mileage')
    date = request.POST.get('date')
    comment = request.POST.get('comment')
    isInvoiced = request.POST.get('isInvoiced')
    isStoraged = request.POST.get('isStoraged')

    salesList = SalesList(salesListID=salesListID, customName=customName, customID=customID,
                          purchaseID=purchaseID, category=category, tractorID=tractorID, trailerID=trailerID,
                          driverName=driverName, supercargo=supercargo, count=count, unitPrice=unitPrice,
                          mileage=mileage, date=date, comment=comment, isInvoiced=isInvoiced, isStoraged=isStoraged)

    if mode == 'add':
        SalesListDBUtils.add(salesList)
        return HttpResponse("OK")

    if mode == 'del' and editId:
        SalesListDBUtils.delete(editId)
        return HttpResponse("OK")

    if mode == 'edit' and editId:
        SalesListDBUtils.update(editId, salesList)
        return HttpResponse("OK")


@csrf_exempt
def editMaterialPurchaseManage(request):
    mode = request.POST.get('oper')

    editId = request.POST.get('id')
    purchaseID = request.POST.get('purchaseID')
    supplierName = request.POST.get('supplierName')
    category = request.POST.get('category')
    tractorID = request.POST.get('tractorID')
    trailerID = request.POST.get('trailerID')
    driverName = request.POST.get('driverName')
    supercargo = request.POST.get('supercargo')
    count = request.POST.get('count')
    unitPrice = request.POST.get('unitPrice')
    mileage = request.POST.get('mileage')
    date = request.POST.get('date')
    isStoraged = request.POST.get('isStoraged')

    materialPurchase = MaterialPurchase(purchaseID=purchaseID, supplierName=supplierName,
                                              category=category, tractorID=tractorID,
                                              trailerID=trailerID, driverName=driverName,
                                              supercargo=supercargo, count=count,
                                              unitPrice=unitPrice, mileage=mileage,
                                              date=date, isStoraged=isStoraged)

    if mode == 'add':
        MaterialPurchaseDBUtils.add(materialPurchase)
        return HttpResponse("OK")

    if mode == 'del' and editId:
        MaterialPurchaseDBUtils.delete(editId)
        return HttpResponse("OK")

    if mode == 'edit' and editId:
        MaterialPurchaseDBUtils.update(editId, materialPurchase)
        return HttpResponse("OK")


@csrf_exempt
def editVehicleMaintenanceManage(request):
    mode = request.POST.get('oper')

    editId = request.POST.get('id')
    vehicleType = request.POST.get('vehicleType')
    vehicleID = request.POST.get('vehicleID')
    maintenanceDate = request.POST.get('maintenanceDate')
    maintenanceItems = request.POST.get('maintenanceItems')
    maintenanceCost = request.POST.get('maintenanceCost')
    maintenanceComment = request.POST.get('maintenanceComment')

    vehicleMaintenanceManage = VehicleMaintenanceManage(vehicleType=vehicleType, vehicleID=vehicleID,
                                                        maintenanceDate=maintenanceDate,
                                                        maintenanceItems=maintenanceItems,
                                                        maintenanceCost=maintenanceCost,
                                                        maintenanceComment=maintenanceComment)

    if mode == 'add':
        VehicleMaintenanceManageDBUtils.add(vehicleMaintenanceManage)
        return HttpResponse("OK")

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

    wastageManage = WastageManage(trailerID=trailerID, wastageCount=wastageCount)

    if mode == 'add':
        WastageManageDBUtils.add(wastageManage)
        return HttpResponse("OK")

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
    balance = request.POST.get('balance')

    customPaymentInfo = CustomPaymentInfo(customName=customName, payTime=payTime, payAmount=payAmount, balance=balance)

    if mode == 'add':
        CustomPaymentInfoDBUtils.add(customPaymentInfo)
        return HttpResponse("OK")

    if mode == 'del' and editId:
        CustomPaymentInfoDBUtils.delete(editId)
        return HttpResponse("OK")

    if mode == 'edit' and editId:
        CustomPaymentInfoDBUtils.update(editId, customPaymentInfo)
        return HttpResponse("OK")

# def monthWastage(request):
#     return render(request,"monthWastage.html")
#
# def saleform(request):
#     return render(request,"saleform.html")


@csrf_exempt
def editUser(request):
    mode = request.POST.get('oper')

    editId = request.POST.get('id')
    userName = request.POST.get('userName')
    userPassword = request.POST.get('userPassword')
    userLevel = request.POST.get('userLevel')

    user = User(userName=userName, userPassword=EncodeUtils.encode(userPassword), userLevel=userLevel)

    if mode == 'add':
        UserDBUtils.add(user)
        return HttpResponse("OK")

    if mode == 'del' and editId:
        UserDBUtils.delete(editId)
        return HttpResponse("OK")

    if mode == 'edit' and editId:
        UserDBUtils.update(editId, user)
        return HttpResponse("OK")
