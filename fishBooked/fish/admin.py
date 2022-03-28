from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

class RadioItemsInline(admin.StackedInline):
    model = RadioItems
class PickerItemsInline(admin.StackedInline):
    model = PickerItems
class CheckboxItemsInline(admin.StackedInline):
    model = CheckboxItems
class ProductDetailInline(admin.StackedInline):
    model = ProductDetail
class ProductAbstractInline(admin.StackedInline):
    model = ProductAbstract
class OrderInline(admin.StackedInline):
    model = Order
class ImageItemsInline(admin.StackedInline):
    model = ImageItems
class advertisingInfoInline(admin.StackedInline):
    model = advertisingInfo
#
class UserInformationAddInline(admin.StackedInline):
    model = UserInformationAdd
class UserInformationAddAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserInformationAdd,UserInformationAddAdmin)
class UserAdmin(BaseUserAdmin):
    inlines = [UserInformationAddInline,ProductAbstractInline]
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
class AccountUserAdmin(admin.ModelAdmin):
    #,'zone'
    list_display = ('name','mobile',)
    search_fields = ['name','mobile']
    ordering = ['province','city']
admin.site.register(AccountUser,AccountUserAdmin)
#ZoneSelect
class ZoneSelectAdmin(admin.ModelAdmin):
    list_display = ('name','address',)
    ordering = ['name']
admin.site.register(ZoneSelect,ZoneSelectAdmin)

class advertisingInfoAdmin(admin.ModelAdmin):
    list_display = ('advertiser','banner_images',)
    ordering = ['advertiser']
admin.site.register(advertisingInfo,advertisingInfoAdmin)

# class advertisingAdmin(admin.ModelAdmin):
#     list_display = ('Product',)
#     ordering = ['Product']
#     inlines = [advertisingInfoInline]
# admin.site.register(advertising,advertisingAdmin)
class ProductAbstractAdmin(admin.ModelAdmin):
    list_display = ('id','title','centent','zone','productType')
    ordering = ['title']
    inlines = [advertisingInfoInline,ProductDetailInline]
    def get_queryset(self, request):
        fqs = super(ProductAbstractAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return fqs
        elif request.user.is_staff:
            #products = ProductAbstract.objects.filter(ManagerUser__username=request.user)
            fqs = fqs.filter(ManagerUser__username=request.user)
            return fqs
admin.site.register(ProductAbstract,ProductAbstractAdmin)

class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ('product','selectType','order','placeholder',"order_count")
    search_fields = ['product']
    list_filter = ('selectType',)
    ordering = ['product','order','selectType']
    inlines = [RadioItemsInline,PickerItemsInline,CheckboxItemsInline]
    fields=('product', ('selectType', 'order'), 'placeholder', 'image',)
    def get_queryset(self, request):
        fqs = super(ProductDetailAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return fqs
        elif request.user.is_staff:
            #products = ProductAbstract.objects.filter(ManagerUser__username=request.user)
            fqs = fqs.filter(product__ManagerUser__username=request.user)
            return fqs

    def order_count(self,obj):
        fpa=ProductAbstract.objects.get(title=obj)
        fq=ProductDetail.objects.filter(product=fpa.id).all()
        count_order=[i.order for i in fq]
        return count_order

admin.site.register(ProductDetail,ProductDetailAdmin)
class ImageItemsAdmin(admin.ModelAdmin):
    list_display = ('image_name','image_select',)
    search_fields = ['image_name']
    ordering = ['image_name']
admin.site.register(ImageItems,ImageItemsAdmin)
class RadioItemsAdmin(admin.ModelAdmin):
    list_display = ('name','value',)
    search_fields = ['name']
    ordering = ['name','value']
admin.site.register(RadioItems,RadioItemsAdmin)
class PickerItemsAdmin(admin.ModelAdmin):
    list_display = ('value',)
    search_fields = []
    ordering = ['value']
admin.site.register(PickerItems,PickerItemsAdmin)
class CheckboxItemsAdmin(admin.ModelAdmin):
    list_display = ('name','value',)
    search_fields = ['name']
    ordering = ['name','value']
admin.site.register(CheckboxItems,CheckboxItemsAdmin)
'''
list_filter = (
        ('author', admin.RelatedOnlyFieldListFilter),
    )
'''
# class ProductDetailAdmin(admin.ModelAdmin):
#     list_display = ('product','type','name','placeholder','prompt')
#     search_fields = ['product','name']
#     list_filter = ('type',)
#     ordering = ['type','name']
#     #inlines = [RadioItemsInline,PickerItemsInline,CheckboxItemsInline]
# admin.site.register(ProductDetail,ProductDetailAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('SubmitUser','product','create_time','submit1','submit2','submit3','submit4','submit5')
    list_filter = (('product',admin.RelatedOnlyFieldListFilter),'create_time')
    ordering = ['product','submit1']
    actions = ['make_csv']
    date_hierarchy = 'create_time'
    def get_queryset(self, request):
        # try:
        #     selected_data=dict(request.POST)
        #     if selected_data['_selected_action']:
        #         selected=selected_data['_selected_action']
        # except:
        #     print('继续吧')
        fqs = super(OrderAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return fqs
        elif request.user.is_staff:
            #products = ProductAbstract.objects.filter(ManagerUser__username=request.user)
            fqs = fqs.filter(product__ManagerUser__username=request.user)
            return fqs
    # queryset.update(status='p')

admin.site.register(Order,OrderAdmin)

from django.shortcuts import get_list_or_404
def make_csv(self, request, queryset):
    #csv_data = self.get_queryset(request).values()
    # selected_data = dict(request.POST)['_selected_action']
    data = queryset.values()
    selected_data = dict(request.POST)['_selected_action']
    csv_data=[]
    for d in data:
        if str(d['id']) in selected_data:
            csv_data.append(d)
    import csv
    from django.http import HttpResponse
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="your_file.csv"'
    writer = csv.writer(response)
    writer.writerow(csv_data[0].keys())
    for xz in range(len(csv_data)):
        writer.writerow(csv_data[xz].values())
    return response
admin.site.add_action(make_csv, 'csv文件下载')

#UserInformationAdd
