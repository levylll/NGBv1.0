#coding:utf-8
from django.db import models
from django.conf import settings

#引入Article Model
from blog.models import Article

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
STATUS = {
        0: u'正常',
        1: u'草稿',
        2: u'删除',
}

class FilmPack(models.Model):
    name = models.CharField(max_length=40,verbose_name=u'产品名称',unique=True)
    en_name = models.CharField(max_length=40,verbose_name=u'产品标识',help_text=u'系统内部标识，不可重复,只能用数字或者字母',unique=True)
    price = models.FloatField(default=0,verbose_name=u'价格')
    summary = models.TextField(blank=True,null=True,verbose_name=u'摘要')
    rank = models.IntegerField(default=0,verbose_name=u'排序')
    status = models.IntegerField(default=0,choices=STATUS.items(),verbose_name='状态')

    create_time = models.DateTimeField(u'创建时间',auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = u'产品包创建'
        ordering = ['rank','-create_time']
        app_label = string_with_title('business',u"2->产品管理")

    
    def __unicode__(self):
        return self.name


class PackContent(models.Model):
    name = models.ForeignKey(FilmPack,verbose_name=u'产品包', related_name='name_PackContent')
    article = models.ForeignKey(Article,verbose_name=u'影片', related_name='article_PackContent')
    create_time = models.DateTimeField(u'创建时间',auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = u'产品包内容'
        unique_together = (("name", "article"),)
        # ordering = ['customer']
        app_label = string_with_title('business',u"2->产品管理")

    def __unicode__(self):
        return self.name.name

class BoughtPack(models.Model):
    name = models.ForeignKey(FilmPack,verbose_name=u'产品包')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=u'用户')
    bought_time = models.DateTimeField(u'购买时间',auto_now=True)

    class Meta:
        verbose_name_plural = verbose_name = u'产品包购买'
        unique_together = (("name", "customer"),)
        # ordering = ['customer']
        app_label = string_with_title('business',u"2->产品管理")

    def __unicode__(self):
        return self.name.name