from django.shortcuts import render
import datetime
import json
import ast
from apps.BaseModels.models import CustomerManage,StaffManage,GasManage,TrailerManage,Supplier,TractorManage
from apps.BussinessModels.models import SalesList,VehicleMaintenanceManage,WastageManage,MaterialPurchase,CustomPaymentInfo
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponse

def json_default(value):
    if isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    else:
        return value.__dict__



# print(json.dumps(CustomerManage.objects.get(id=1), default=json_default))



def index(request):
    return render(request, "index.html")

def homePage(request):
    return render(request, "homePage.html")

def unfound(request):
    return render(request, "404.html")

def carfixManage(request):
    return render(request,"carfixManage.html")


def staffManage(request):
    allStaffs = []
    for staff in StaffManage.objects.all():
        aa = json.dumps(staff, default=json_default)
        bb = json.loads(aa)
        allStaffs.append(bb)

    return render(request, "staffManage.html" ,{'showData': json.dumps(allStaffs)})


def gasManage(request):
    allGas = []
    for gas in GasManage.objects.all():
        aa = json.dumps(gas, default=json_default)
        bb = json.loads(aa)
        allGas.append(bb)

    return render(request, "gasManage.html" ,{'showData': json.dumps(allGas)})

def customManage(request):
    allCustom = []
    for a in CustomerManage.objects.all():
        # 获取字符串
        aa = json.dumps(a, default=json_default)
        bb = json.loads(aa)
        # print(bb)
        allCustom.append(bb)
        # allCustom.append(json.dumps(a, default=json_default))
    return render(request,"customManage.html" ,  {'showData': json.dumps(allCustom)})

def trailerManage(request):
    allTrailer = []
    for trailer in TrailerManage.objects.all():
        aa = json.dumps(trailer, default=json_default)
        bb = json.loads(aa)
        allTrailer.append(bb)

    return render(request, "trailerManage.html" ,{'showData': json.dumps(allTrailer)})

def tractorManage(request):
    allTractor = []
    for tractor in TractorManage.objects.all():
        aa = json.dumps(tractor,default=json_default)
        bb = json.loads(aa)
        allTractor.append(bb)
    return render(request, "tractorManage.html", {'showData': json.dumps(allTractor)})

def supplier(request):
    allSupplier = []
    for supplier in Supplier.objects.all():
        aa = json.dumps(supplier, default=json_default)
        bb = json.loads(aa)
        allSupplier.append(bb)

    return render(request, "supplier.html" ,{'showData': json.dumps(allSupplier)})

def salesList(request):
    allSalesList = []
    for salesList in Supplier.objects.all():
        aa = json.dumps(salesList, default=json_default)
        bb = json.loads(aa)
        allSalesList.append(bb)

    return render(request, "salesList.html" ,{'showData': json.dumps(allSalesList)})


def vehicleMaintenanceManage(request):
    allVehicleMaintenanceManage = []
    for vehicleMaintenanceManage in Supplier.objects.all():
        aa = json.dumps(salesList, default=json_default)
        bb = json.loads(aa)
        allVehicleMaintenanceManage.append(bb)

    return render(request, "vehicleMaintenanceManage.html" ,{'showData': json.dumps(allVehicleMaintenanceManage)})

def wastageManage(request):
    allWastageManage = []
    for wastageManage in WastageManage.objects.all():
        aa = json.dumps(wastageManage, default=json_default)
        bb = json.loads(aa)
        allWastageManage.append(bb)

    return render(request, "wastageManage.html" ,{'showData': json.dumps(allWastageManage)})

def materialPurchase(request):
    allmaterialPurchase = []
    for materialpurchase in MaterialPurchase.objects.all():
        aa = json.dumps(materialpurchase, default=json_default)
        bb = json.loads(aa)
        allmaterialPurchase.append(bb)

    return render(request, "materialPurchase.html", {'showData': json.dumps(allmaterialPurchase)})



def customPaymentInfo(request):
    allCustomPaymentInfo = []
    for customPaymentInfo in CustomPaymentInfo.objects.all():
        aa = json.dumps(customPaymentInfo, default=json_default)
        bb = json.loads(aa)
        allCustomPaymentInfo.append(bb)

    return render(request, "customPaymentInfo.html" ,{'showData': json.dumps(allCustomPaymentInfo)})

@csrf_exempt
def editCustomManage(request):
     # mode = request.get()
     mode = request.POST.get('oper','')
     if mode == 'add' :
         customID = request.POST.get('customID', '')
         customName = request.POST.get('customName', '')
         tel = request.POST.get('tel', '')
         addr = request.POST.get('addr', '')
         taxFileNO = request.POST.get('taxFileNO', '')
         bankOfDepsit = request.POST.get('bankOfDepsit', '')
         bankAccount = request.POST.get('bankAccount', '')
         fax = request.POST.get('fax', '')
         industryField = request.POST.get('industryField', '')
         companyNature = request.POST.get('companyNature', '')
         consocationMode = request.POST.get('consocationMode', '')
         level = request.POST.get('level', '')
         contract = request.POST.get('contract', '')
         payCycle = request.POST.get('payCycle', '')
         companyCharge = request.POST.get('companyCharge', '')
         companyContact = request.POST.get('companyContact', '')
         customQualification = request.POST.get('customQualification', '')
         annualSales = request.POST.get('annualSales', '')

         b = CustomerManage(customID= customID, customName= customName ,tel=tel,addr=addr,taxFileNO=taxFileNO, bankOfDepsit=bankOfDepsit,bankAccount = bankAccount ,  fax=fax,
                            industryField = industryField, companyNature=companyNature, consocationMode=consocationMode, level=level, contract=contract,payCycle=payCycle,
                            companyCharge=companyCharge,companyContact =companyContact , customQualification =customQualification, annualSales=annualSales)
         b.save()
         return 1

     if mode == 'del':
         customID = request.POST.get('customID', '')


     if mode == 'edit':
         customID = request.POST.get('customID', '')
         customName = request.POST.get('customName', '')
         tel = request.POST.get('tel', '')
         addr = request.POST.get('addr', '')
         taxFileNO = request.POST.get('taxFileNO', '')
         bankOfDepsit = request.POST.get('bankOfDepsit', '')
         bankAccount = request.POST.get('bankAccount', '')
         fax = request.POST.get('fax', '')
         industryField = request.POST.get('industryField', '')
         companyNature = request.POST.get('companyNature', '')
         consocationMode = request.POST.get('consocationMode', '')
         level = request.POST.get('level', '')
         contract = request.POST.get('contract', '')
         payCycle = request.POST.get('payCycle', '')
         companyCharge = request.POST.get('companyCharge', '')
         companyContact = request.POST.get('companyContact', '')
         customQualification = request.POST.get('customQualification', '')
         annualSales = request.POST.get('annualSales', '')

     return 1 ;


@csrf_exempt
def editStaffManage(request):
    mode = request.POST.get('oper', '')
    if mode == 'add':
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

        staff.save()

    # return 这里有问题需要修改，这里应该返回一个httpresponse对象，但是还不确定这里该返回一个怎样的httpresponse对象
    # 待修改
    return HttpResponse("OK")


@csrf_exempt
def editGasManage(request):
    mode = request.POST.get('oper', '')
    if mode == 'add':
        gasID = request.POST.get('gasID')
        gasName = request.POST.get('gasName')

        gas = GasManage(gasID=gasID, gasName=gasName)

        gas.save()

    # return 这里有问题需要修改，这里应该返回一个httpresponse对象，但是还不确定这里该返回一个怎样的httpresponse对象
    # 待修改
    return HttpResponse("OK")

@csrf_exempt
def editTrailerManage(request):
    mode = request.POST.get('oper', '')
    if mode == 'add':
        trailerID= request.POST.get('trailerID')
        annualInspectionTime = request.POST.get('annualInspectionTime')
        insuranceTime = request.POST.get('insuranceTime')
        chassisNumber = request.POST.get('chassisNumber')
        deliveryTime = request.POST.get('deliveryTime')

        trailer = TrailerManage(trailerID=trailerID, annualInspectionTime=annualInspectionTime, insuranceTime=insuranceTime, chassisNumber=chassisNumber, deliveryTime=deliveryTime)

        trailer.save()

    # return 这里有问题需要修改，这里应该返回一个httpresponse对象，但是还不确定这里该返回一个怎样的httpresponse对象
    # 待修改
    return HttpResponse("OK")

@csrf_exempt
def editTractorManage(request):
    mode = request.POST.get('oper', '')
    if mode == 'add':
        tractorID= request.POST.get('tractorID')
        annualInspectionTime = request.POST.get('annualInspectionTime')
        insuranceTime = request.POST.get('insuranceTime')
        chassisNumber = request.POST.get('chassisNumber')
        deliveryTime = request.POST.get('deliveryTime')

        tractor = TractorManage(tractorID=tractorID, annualInspectionTime=annualInspectionTime, insuranceTime=insuranceTime, chassisNumber=chassisNumber, deliveryTime=deliveryTime)

        tractor.save()

    # return 这里有问题需要修改，这里应该返回一个httpresponse对象，但是还不确定这里该返回一个怎样的httpresponse对象
    # 待修改
    return HttpResponse("OK")



@csrf_exempt
def editSupplier(request):
    mode = request.POST.get('oper', '')
    if mode == 'add':
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

        supplier = Supplier(supplierID=supplierID, supplierName=supplierName,tel=tel,addr=addr,companyChargeName=companyChargeName,companyChargePosition=companyChargePosition,
                            companyChargeTel=companyChargeTel,companyContactName=companyContactName,companyContactPosition=companyContactPosition,companyContactTel=companyContactTel,
                            customQualification=customQualification,customTaxFileNO=customTaxFileNO,customBankOfDepsit=customBankOfDepsit,customBankAccount=customBankAccount,
                            customContactName=customContactName,customContactTel=customContactTel,purchaseCategory=purchaseCategory
                            )

        supplier.save()

    # return 这里有问题需要修改，这里应该返回一个httpresponse对象，但是还不确定这里该返回一个怎样的httpresponse对象
    # 待修改
    return HttpResponse("OK")



@csrf_exempt
def editSalesList(request):
    mode = request.POST.get('oper', '')
    if mode == 'add':
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

        salesList = SalesList(salesListID=salesListID, customName=customName,customID=customID,
                              purchaseID=purchaseID,category=category,tractorID=tractorID,trailerID=trailerID,
                              driverName=driverName,supercargo=supercargo,count=count,unitPrice=unitPrice,
                              mileage=mileage,date=date,comment=comment,isInvoiced=isInvoiced,isStoraged=isStoraged
                            )

        salesList.save()

    # return 这里有问题需要修改，这里应该返回一个httpresponse对象，但是还不确定这里该返回一个怎样的httpresponse对象
    # 待修改
    return HttpResponse("OK")


@csrf_exempt
def editVehicleMaintenanceManage(request):
    mode = request.POST.get('oper', '')
    if mode == 'add':
        vehicleType= request.POST.get('vehicleType')
        vehicleID = request.POST.get('vehicleID')
        maintenanceDate = request.POST.get('maintenanceDate')
        maintenanceItems = request.POST.get('maintenanceItems')
        maintenanceCost = request.POST.get('maintenanceCost')
        maintenanceComment = request.POST.get('maintenanceComment')

        vehicleMaintenanceManage = VehicleMaintenanceManage(vehicleType=vehicleType, vehicleID=vehicleID, maintenanceDate=maintenanceDate,
                                maintenanceItems=maintenanceItems, maintenanceCost=maintenanceCost,maintenanceComment=maintenanceComment)

        vehicleMaintenanceManage.save()

    # return 这里有问题需要修改，这里应该返回一个httpresponse对象，但是还不确定这里该返回一个怎样的httpresponse对象
    # 待修改
    return HttpResponse("OK")

@csrf_exempt
def editWastageManage(request):
    mode = request.POST.get('oper', '')
    if mode == 'add':
        trailerID= request.POST.get('trailerID')
        wastageCount = request.POST.get('wastageCount')

        wastageManage = WastageManage(trailerID=trailerID, wastageCount=wastageCount)

        wastageManage.save()

    # return 这里有问题需要修改，这里应该返回一个httpresponse对象，但是还不确定这里该返回一个怎样的httpresponse对象
    # 待修改
    return HttpResponse("OK")

@csrf_exempt
def editmaterialPurchaseManage(request):
    mode = request.POST.get('oper', '')
    if mode == 'add':
        purchaseID= request.POST.get('purchaseID')
        supplierName= request.POST.get('supplierName')
        category = request.POST.get('category')
        tractorID = request.POST.get('tractorID')
        trailerID = request.POST.get('trailerID')
        driverName= request.POST.get('driverName')
        supercargo = request.POST.get('supercargo')
        count = request.POST.get('count')
        unitPrice = request.POST.get('unitPrice')
        mileage = request.POST.get('mileage')
        date = request.POST.get('date')
        isStoraged = request.POST.get('isStoraged')

        materialPurchaseManage = MaterialPurchase(purchaseID=purchaseID,supplierName=supplierName,
                                                  category=category,tractorID=tractorID,
                                                  trailerID=trailerID,driverName=driverName,
                                                  supercargo=supercargo,count=count,
                                                  unitPrice=unitPrice,mileage=mileage,
                                                  date=date,isStoraged=isStoraged)


        materialPurchaseManage.save()

    # return 这里有问题需要修改，这里应该返回一个httpresponse对象，但是还不确定这里该返回一个怎样的httpresponse对象
    # 待修改
    return HttpResponse("OK")

@csrf_exempt
def editCustomPaymentInfo(request):
    mode = request.POST.get('oper', '')
    if mode == 'add':
        customName= request.POST.get('customName')
        payTime = request.POST.get('payTime')
        payAmount= request.POST.get('payAmount')
        balance = request.POST.get('balance')

        customPaymentInfo = CustomPaymentInfo(customName=customName, payTime=payTime,payAmount=payAmount,balance=balance)

        customPaymentInfo.save()

    # return 这里有问题需要修改，这里应该返回一个httpresponse对象，但是还不确定这里该返回一个怎样的httpresponse对象
    # 待修改
    return HttpResponse("OK")


def materialPurchase(request):
    return render(request,"materialPurchase.html")

def monthWastage(request):
    return render(request,"monthWastage.html")

def saleform(request):
    return render(request,"saleform.html")