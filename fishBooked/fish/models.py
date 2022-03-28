
# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token
#
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
from django.db import models
from datetime import datetime
from fishBooked import settings
from django.contrib.auth.models import User

'''
为了能够
1 在填写的时候使用选择字段
2 这个字段可以在后台管理系统自定义
步骤：
1 排除zone = models.CharField(max_length=200,choices=select_a_zone(),blank=True, null=True)
    的字段和表都makemigrations和migrate了，如果不先处理他们的话会报“没有fish_zoneselect表”。
    根据报错我先处理其他表再处理zone字段。这个方法可行。
2 makemigrations和migrate字段zone
说明：在zone中设置default='未选择'在后台管理系统就能不能使用选择器。
'''

class ZoneSelect(models.Model):
    name = models.CharField(max_length=100,help_text='区的名称，比如“长安大学渭水校区”用于做区分')
    x_coordinate = models.FloatField(blank=True,null=True,help_text='横坐标')
    y_coordinate = models.FloatField(blank=True,null=True,help_text='纵坐标')
    address = models.CharField(max_length=300,blank=True,null=True)
    def __str__(self):
        return str(self.name)
    class Meta:
        verbose_name = '位置'
        verbose_name_plural = verbose_name

# from django.contrib.auth.models import AbstractUser
# class UserProfile(AbstractUser):
#     def __str__(self):
#         return str(self.username)
#     class Meta:
#         verbose_name = "用户信息"
#         verbose_name_plural = verbose_name

def select_a_zone(self=ZoneSelect):
    select_objects = self.objects.all()
    zip_zone = tuple((str(i), '{}'.format(i)) for i in select_objects)
    return zip_zone
class AccountUser(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    province = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    detail = models.CharField(max_length=100, blank=True, null=True)
    zone = models.CharField(max_length=200,choices=select_a_zone(),blank=True, null=True)
    the_index=models.CharField(max_length=20,blank=True,null=True)
    create_time = models.DateTimeField(default=datetime.now())
    def __str__(self):
        return str(self.name)
    class Meta:
        verbose_name = '账户信息'
        verbose_name_plural = verbose_name
        db_table = 'account_user_address'


#select_a_zone(AccountUser)
#https://docs.djangoproject.com/en/1.11/topics/migrations/#migration-serializing
class ProductAbstract(models.Model):
    PRODUCT_TYPE_CHOICE=(
        ('商品类型1','商品类型1'),
        ('商品类型2','商品类型2'),
        ('商品类型3','商品类型3'),
        ('商品类型4','商品类型4')
    )
    ManagerUser = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    zone = models.CharField(max_length=200, choices=select_a_zone(), blank=True, null=True)
    productType = models.CharField(blank=True, null=True, max_length=100, choices=PRODUCT_TYPE_CHOICE)
    title = models.CharField(max_length=100)
    centent = models.TextField(max_length=1000)
    #explaintext = models.TextField( blank=True, null=True,help_text="为了给用户提示信息的，这应该在文末，并且管理端填写")
    headImage = models.ForeignKey('ImageItems',on_delete=models.CASCADE,blank=True, null=True)
    def __str__(self):
        return str(self.title)
    class Meta:
        verbose_name = '商品介绍'
        verbose_name_plural = verbose_name

class ImageItems(models.Model):
    image_name = models.CharField(default='',max_length=100)
    image_select = models.ImageField(upload_to='static/images/%Y/%m/%d')#应该上传到云端才对
    #ProductAbstract = models.ForeignKey('ProductAbstract',on_delete=models.CASCADE)
    def __str__(self):
        return str(self.image_name)
    class Meta:
        verbose_name = '图片集合'
        verbose_name_plural = verbose_name


class ProductDetail(models.Model):
    TYPE_CHOICE = (
        ('text','text'),
        ('textarea','textarea'),
        ('picker','picker'),
        ('radio','radio'),
        ('checkbox','checkbox'),
        ('image', 'image'),
        ('picker-view', 'picker-view'),
        ('slider', 'slider'),
        ('switch', 'switch'),
        ('progress', 'progress'),
        ('video', 'video'),
        ('rich-text', 'rich-text'),
        ('show-picture','show-picture'),
        ('show-text','show-text'),
        ('show-title','show-title')
    )
    product = models.ForeignKey(
        ProductAbstract,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    selectType = models.CharField(blank=True, null=True,max_length=100,choices=TYPE_CHOICE)
    order = models.CharField(max_length=100, blank=True, null=True,help_text="起排序作用的")
    placeholder = models.TextField(max_length=300, blank=True, null=True,help_text="占位符，起提示作用")
    prompt = models.TextField(max_length=300, blank=True, null=True,help_text="会根据selectType自动添加组件name或value")
    image=models.ForeignKey(ImageItems,on_delete=models.CASCADE,blank=True,null=True,help_text='selectType=show-image时填写')
    def __str__(self):
        return str(self.product)
    class Meta:
        unique_together=('product','order',)
        verbose_name = '商品内部页面'
        verbose_name_plural = verbose_name




class RadioItems(models.Model):
    name = models.CharField(default='',max_length=100)
    value = models.CharField(default='',max_length=100)
    ProductDetail = models.ForeignKey('ProductDetail', blank=True, null=True, on_delete=models.CASCADE,
                                   help_text="关联radio选项需要的name和value")
    def __str__(self):
        return str(self.name)
    class Meta:
        verbose_name = 'radio单选框'
        verbose_name_plural = verbose_name

class PickerItems(models.Model):
    value = models.CharField(default='',max_length=100)
    ProductDetail= models.ForeignKey('ProductDetail', blank=True, null=True, on_delete=models.CASCADE,
                                    help_text="关联picker选项需要array数组，是一组value")
    def __str__(self):
        return str(self.value)
    class Meta:
        verbose_name = 'picker选择器'
        verbose_name_plural = verbose_name

class CheckboxItems(models.Model):
    name = models.CharField(default='',max_length=100)
    value = models.CharField(default='',max_length=100)
    ProductDetail = models.ForeignKey('ProductDetail', blank=True, null=True, on_delete=models.CASCADE,
                                      help_text="关联checkbox选项需要的name和value")
    def __str__(self):
        return str(self.name)
    class Meta:
        verbose_name = 'checkbox复选框'
        verbose_name_plural = verbose_name





# class ProductDetail(models.Model):
#     TYPE_CHOICE = (
#         ('text', 'textType'),
#         ('textarea', 'textareaType'),
#         ('picker', 'pickerType'),
#         ('radio', 'radioType'),
#         ('explain', 'explainType'),
#         ('image', 'imageType'),
#         ('checkbox', 'checkboxType')
#     )
#     product = models.ForeignKey(
#         ProductAbstract,
#         on_delete=models.CASCADE,
#         blank=True,
#         null=True
#     )
#     type = models.CharField(max_length=100, choices=TYPE_CHOICE)
#     name = models.CharField(max_length=100, blank=True, null=True, help_text="起排序作用的，起名叫name是为了对应小程序中属性名称")
#     placeholder = models.CharField(max_length=300, blank=True, null=True, help_text="text,textarea类的才有这个属性")
#     prompt = models.CharField(max_length=300, blank=True, null=True,
#                                 help_text="就是提示这个选择是用来干嘛的，总不能一堆空白让人选呀，text和textarea好歹还有placeholder用来提示")
#
#     def __str__(self):
#         return str(self.product)
#
#     class Meta:
#         unique_together = ('product', 'name',)
#         verbose_name = '商品内部页面'
#         verbose_name_plural = verbose_name

#     radio_items = models.ForeignKey(RadioItems, blank=True, null=True, on_delete=models.CASCADE)
#     picker_items = models.ForeignKey(PickerItems, blank=True, null=True, on_delete=models.CASCADE)
#     checkbox_items = models.ForeignKey(CheckboxItems, blank=True, null=True, on_delete=models.CASCADE)



class Order(models.Model):
    SubmitUser = models.ForeignKey(User,blank=True,null=True, on_delete=models.CASCADE)
    product = models.ForeignKey('ProductAbstract',on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=datetime.now(),blank=True, null=True)
    submit1 = models.CharField(max_length=100,default='',blank=True, null=True)
    submit2 = models.CharField(max_length=100,default='',blank=True, null=True)
    submit3 = models.CharField(max_length=100,default='',blank=True, null=True)
    submit4 = models.CharField(max_length=100,default='',blank=True, null=True)
    submit5 = models.CharField(max_length=100,default='',blank=True, null=True)
    submit6 = models.CharField(max_length=100,default='',blank=True, null=True)
    submit7 = models.CharField(max_length=100,default='',blank=True, null=True)
    submit8 = models.CharField(max_length=100,default='',blank=True, null=True)
    submit9 = models.CharField(max_length=100,default='',blank=True, null=True)
    submit10 = models.CharField(max_length=100,default='',blank=True, null=True)
    submit11 = models.CharField(max_length=100,default='',blank=True, null=True)
    submit12 = models.CharField(max_length=100,default='',blank=True, null=True)
    submit13 = models.CharField(max_length=100,default='',blank=True, null=True)
    submit14 = models.CharField(max_length=100,default='',blank=True, null=True)
    submit15 = models.CharField(max_length=100,default='',blank=True, null=True)
    submit16 = models.CharField(max_length=100,default='',blank=True, null=True)
    submit17 = models.CharField(max_length=100,default='',blank=True, null=True)
    submit18 = models.CharField(max_length=100,default='',blank=True, null=True)
    submit19 = models.CharField(max_length=100,default='',blank=True, null=True)
    submit20 = models.CharField(max_length=100,default='',blank=True, null=True)
    def __str__(self):
        return str(self.product)
    class Meta:
        verbose_name = '用户提交的表单'
        verbose_name_plural = verbose_name

#orderImage还没有起作用，无用状态，需要能处理微信服务器传来的图片连接才行
class OrderImage(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.CASCADE)
    filePath = models.ImageField(upload_to='static/up_images')
    create_time = models.DateTimeField(default=datetime.now(), blank=True, null=True)
    def __str__(self):
        return str(self.order)
    class Meta:
        verbose_name = 'order关联的图片'
        verbose_name_plural = verbose_name

class UserInformationAdd(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    phone_number= models.CharField(verbose_name='电话号码',max_length=100,default='',blank=True, null=True)
    #really_name = models.CharField(verbose_name='姓名',max_length=100,default='',blank=True, null=True)
    address = models.CharField(verbose_name='住址',max_length=100,default='',blank=True, null=True)
    def __str__(self):
        return str(self.user)
    class Meta:
        verbose_name = '管理员用户更多的信息'
        verbose_name_plural = verbose_name

class advertisingInfo(models.Model):
    advertiser = models.ForeignKey('ProductAbstract', blank=True, null=True, on_delete=models.CASCADE)
    banner_images= models.ImageField(blank=True, null=True,upload_to='static/advertising/%Y/%m/%d')
    def __str__(self):
        return str(self.advertiser)
    class Meta:
        verbose_name = '广告信息'
        verbose_name_plural = verbose_name
# class advertising(models.Model):
#     Product = models.ForeignKey('ProductAbstract', blank=True, null=True, on_delete=models.CASCADE)
#     def __str__(self):
#         return str(self.Product)
#     class Meta:
#         verbose_name = '广告与商品对应关系'
#         verbose_name_plural = verbose_name



