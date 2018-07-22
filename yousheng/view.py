from django.shortcuts import render
import datetime
import json
import ast
from apps.BaseModels.models import CustomerManage
from django.views.decorators.csrf import csrf_exempt, csrf_protect

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



def materialPurchase(request):
    return render(request,"materialPurchase.html")

def monthWastage(request):
    return render(request,"monthWastage.html")

def saleform(request):
    return render(request,"saleform.html")