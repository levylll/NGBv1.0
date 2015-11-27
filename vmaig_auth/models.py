#coding:utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser

#用来修改admin中显示的app名称,因为admin app 名称是用 str.title()显示的,所以修改str类的title方法就可以实现.
class string_with_title(str):
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self


# Create your models here.

class VmaigUser(AbstractUser):
    img = models.CharField(max_length=200,default='/static/tx/default.jpg',verbose_name=u'头像地址')
    intro = models.CharField(max_length=200,blank=True,null=True,verbose_name=u'简介')
    useraddr = models.CharField(max_length=200,blank=True,null=True,verbose_name=u'联系地址')
    usertel = models.CharField(max_length=200,blank=True,null=True,verbose_name=u'手机号码')
    # userbday = models.DateField(blank=True,null=True,verbose_name=u'生日')
    useracnt = models.FloatField(default=0,verbose_name=u'账户余额')

    class Meta(AbstractUser.Meta):
        verbose_name_plural = verbose_name = u'用户管理'
        app_label = string_with_title('vmaig_auth',u"3->运营支撑")

#购买产品包/影片记录表
class BuyLog(models.Model):
    name = models.CharField(max_length=40,verbose_name=u'产品名称')
    customer = models.CharField(max_length=40,verbose_name=u'用户')
    buy_type = models.CharField(max_length=40,verbose_name=u'类型')
    price = models.FloatField(default=0,verbose_name=u'价格')
    bak = models.TextField(blank=True,null=True,verbose_name=u'备注')
    create_time = models.DateTimeField(u'购买时间',auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = u'购买记录管理'
        ordering = ['-create_time']
        app_label = string_with_title('vmaig_auth',u"3->运营支撑")


    def __unicode__(self):
        return self.name

#充值记录
class ChargeLog(models.Model):
    customer = models.CharField(max_length=40,verbose_name=u'用户')
    money = models.FloatField(default=0,verbose_name=u'充值金额')
    bak = models.TextField(blank=True,null=True,verbose_name=u'备注')
    create_time = models.DateTimeField(u'充值时间',auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = u'充值记录管理'
        ordering = ['-create_time']
        app_label = string_with_title('vmaig_auth',u"3->运营支撑")


    def __unicode__(self):
        return self.name


#操作日志
class OprLog(models.Model):
    name = models.CharField(max_length=40,verbose_name=u'表名')
    customer = models.CharField(max_length=40,verbose_name=u'用户')
    opr_type = models.CharField(max_length=40,verbose_name=u'操作类型')
    create_time = models.DateTimeField(u'操作时间',auto_now_add=True)
    bak = models.TextField(blank=True,null=True,verbose_name=u'备注')

    class Meta:
        verbose_name_plural = verbose_name = u'表级操作记录'
        ordering = ['-create_time']
        app_label = string_with_title('django_extlog',u"5->运维管理")


    def __unicode__(self):
        return self.name

