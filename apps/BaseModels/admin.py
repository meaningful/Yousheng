from django.contrib import admin
from .models import CustomerManage , TractorManage, Supplier ,GasManage ,TrailerManage,StaffManage,UserManage

# Register your models here.
admin.site.register(CustomerManage )
admin.site.register(TractorManage )
admin.site.register(Supplier )
admin.site.register(GasManage )
admin.site.register(TrailerManage )
admin.site.register(StaffManage )
admin.site.register(UserManage )