"""yousheng URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import view

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$', view.index),
    url(r'^homePage.html$', view.homePage),
    url(r'^carfixManage.html$', view.carfixManage),
    url(r'^customManage.html$', view.customManage),
    url(r'^materialPurchase.html$', view.materialPurchase),
    url(r'^editMaterialPurchaseManage', view.editMaterialPurchaseManage),
    # url(r'^monthWastage.html$',view.monthWastage),
    # url(r'^saleform.html$',view.saleform),
    url(r'^404.html$', view.unfound),
    url(r'^editCustomManage$', view.editCustomManage),
    url(r'^staffManage', view.staffManage),
    url(r'^editStaffManage', view.editStaffManage),
    url(r'^gasManage', view.gasManage),
    url(r'^editGasManage', view.editGasManage),
    url(r'^trailerManage', view.trailerManage),
    url(r'^editTrailerManage', view.editTrailerManage),
    url(r'^tractorManage', view.tractorManage),
    url(r'^editTractorManage',view.editTractorManage),
    url(r'^supplier', view.supplier),
    url(r'^editSupplier', view.editSupplier),
    url(r'^salesList', view.salesList),
    url(r'^editSalesList', view.editSalesList),
    url(r'^vehicleMaintenanceManage', view.vehicleMaintenanceManage),
    url(r'^editVehicleMaintenanceManage', view.editVehicleMaintenanceManage),
    url(r'^wastageManage', view.wastageManage),
    url(r'^editWastageManage', view.editWastageManage),
    url(r'^customPaymentInfo', view.customPaymentInfo),
    url(r'^editCustomPaymentInfo', view.editCustomPaymentInfo),
    url(r'^userManage', view.userManage),
    url(r'^editUser', view.editUser),
    url(r'^getAllCustomNames', view.getAllCustomNames),
    url(r'^getAllSupplierNames', view.getAllSupplierNames),
    url(r'^getAllGasName', view.getAllGasName),
    url(r'^getAllTractorIDs', view.getAllTractorIDs),
    url(r'^getTrailerIDs', view.getTrailerIDs),
    url(r'^getAllDriverNames', view.getAllDriverNames),
    url(r'^getAllSupercargoNames', view.getAllSupercargoNames),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOTS)
