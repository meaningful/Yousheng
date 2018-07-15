from django.db import models

# Create your models here.

# <- 客户管理表 Begin ->
# 客户编号		customID
# 名称	单位名称+简称	customName
# 电话		tel
# 地址		addr
# 税号		taxFileNO
# 开户行		bankOfDepsit
# 账号		bankAccount
# 传真		fax
# 所属行业		industryField
# 公司性质		companyNature
# 用气种类	【废弃，不用】	gasCategory
# 储罐大小	【废弃，不用】	gasTankSize
# 合作类型	【直供， 共建，中间站】	consocationMode
# 等级	【A/B/C/D】	level
# 合同	【varchar(256)】 合同号	contract
# 付款周期		payCycle
# 公司负责人		companyCharge
# 公司联系人		companyContact
# 客户资质	三证	customQualification
# 年销售额		annualSales


class CustomerManage(models.Model):
    customID = models.CharField(max_length=100)
    customName = models.CharField(max_length=100)
    tel = models.CharField(max_length=20)
    addr = models.CharField(max_length=100)
    taxFileNO = models.CharField(max_length=100)
    bankOfDepsit = models.CharField(max_length=100)
    bankAccount = models.CharField(max_length=100)
    fax = models.CharField(max_length=100)
    industryField = models.CharField(max_length=100)
    companyNature = models.CharField(max_length=100)
    gasCategory = models.CharField(max_length=100)
    consocationMode = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    contract = models.CharField(max_length=100)
    payCycle = models.DateField()
    companyCharge = models.CharField(max_length=100)
    companyContact = models.CharField(max_length=100)
    customQualification = models.CharField(max_length=100)
    annualSales = models.CharField(max_length=100)


# <- 客户管理表 End ->



# 气体编号 ：gasID
# 气体名称 ：gasName


class GasManage(models.Model):
    gasID = models.CharField(max_length=100)
    gasName = models.CharField(max_length=100)
