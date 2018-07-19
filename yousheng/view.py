from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def homePage(request):
    return render(request, "homePage.html")

def unfound(request):
    return render(request, "404.html")

def carfixManage(request):
    return render(request,"carfixManage.html")

def customManage(request):
    return render(request,"customManage.html")

def materialPurchase(request):
    return render(request,"materialPurchase.html")

def monthWastage(request):
    return render(request,"monthWastage.html")

def saleform(request):
    return render(request,"saleform.html")