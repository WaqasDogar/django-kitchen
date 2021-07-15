from django.contrib import admin
from .models import *
# Register your models here.

class classlogindetails(admin.ModelAdmin):
    list_display=['id','LoginID','Username','Email','LoginTime']
class classOffers(admin.ModelAdmin):
    list_display=['id','OfferName','OfferPrice','Availability','CreateTime']
class classEmployee(admin.ModelAdmin):
    list_display=['id','FirstName','LastName','CNIC','FatherName','Age','Gender','MaritalStatus','EntryDate']
class ClassDelivery(admin.ModelAdmin):
    list_display=['id','EmployeePID','CustomerOrderID','DeliveryAddress','ExpectedTime','EntryDate']
class ClassContactus(admin.ModelAdmin):
    list_display=['id','Name','Email','Message','EntryDate']
class ClassWebResources(admin.ModelAdmin):
    list_display=['id','Location','Phone','Day','OpeningTime','ClosingTime','LinkedInLink','GitLink','TwitterLink','FbLink','EntryDate']
class ClassCEO(admin.ModelAdmin):
    list_display=['id','Image','Name','Rank','EntryDate']
class classproduct(admin.ModelAdmin):
    list_display=['id','name','price','image']


admin.site.register(LoginDetail,classlogindetails)
admin.site.register(Offers,classOffers)
admin.site.register(Employee,classEmployee)
admin.site.register(Delivery,ClassDelivery)
admin.site.register(contactus,ClassContactus)
admin.site.register(WebResources,ClassWebResources)
admin.site.register(CEO,ClassCEO)
admin.site.register(Product,classproduct)

#----cart----

admin.site.register(OrdereProduct)
#-------combine list
class OrderItemInline(admin.TabularInline):
    model = OrdereProduct
    raw_id_fields = ['order']

@admin.register(Req_info)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id']
    #list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
#------endcart-----