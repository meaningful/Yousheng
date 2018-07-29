from django.shortcuts import render
import datetime
import json
import ast
from apps.BaseModels.models import CustomerManage,StaffManage,GasManage,TrailerManage,Supplier
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

def supplier(request):
    allSupplier = []
    for supplier in Supplier.objects.all():
        aa = json.dumps(supplier, default=json_default)
        bb = json.loads(aa)
        allSupplier.append(bb)

    return render(request, "supplier.html" ,{'showData': json.dumps(allSupplier)})

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






def materialPurchase(request):
    return render(request,"materialPurchase.html")

def monthWastage(request):
    return render(request,"monthWastage.html")

def saleform(request):
    return render(request,"saleform.html")