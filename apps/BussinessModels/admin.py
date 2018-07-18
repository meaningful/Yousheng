from django.contrib import admin
from .models import SalesList , MaterialPurchase ,VehicleMaintenanceManage ,WastageManage ,CustomPaymentInfo
# Register your models here.
admin.site.register(SalesList )
admin.site.register(MaterialPurchase )
admin.site.register(VehicleMaintenanceManage )
admin.site.register(WastageManage )
admin.site.register(CustomPaymentInfo )