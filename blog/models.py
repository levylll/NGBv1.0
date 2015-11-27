#coding:utf-8
from django.db import models
from django.conf import settings

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

# 转码状态
CHGSTATUS = {
        0: u'已转码',
        1: u'未转码',
}

#资讯来源
NEWS = {
        0: u'oschina',
        1: u'chiphell',
        2: u'freebuf',
        3: u'cnBeta',
}


class Nav(models.Model):
    name = models.CharField(max_length=40,verbose_name=u'导航条内容')
    url = models.CharField(max_length=200,blank=True,null=True,verbose_name=u'指向地址')

    status = models.IntegerField(default=0,choices=STATUS.items(),verbose_name='状态')
    create_time = models.DateTimeField(u'创建时间',auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = u"导航条"
        ordering = ['-create_time']
        app_label = string_with_title('blog',u"1->媒体资源管理")

    def __unicode__(self):
        return self.name




class Category(models.Model):
    name = models.CharField(max_length=40,verbose_name=u'名称')
    parent = models.ForeignKey('self',default=None,blank=True,null=True,verbose_name=u'上级分类')
    rank = models.IntegerField(default=0,verbose_name=u'排序')
    status = models.IntegerField(default=0,choices=STATUS.items(),verbose_name='状态')

    create_time = models.DateTimeField(u'创建时间',auto_now_add=True)
    class Meta:
        verbose_name_plural = verbose_name = u'分类'
        ordering = ['rank','-create_time']
        app_label = string_with_title('blog',u"1->媒体资源管理")


    def __unicode__(self):
        if self.parent:
            return '%s-->%s' % (self.parent,self.name)
        else:
            return '%s' % (self.name)

#
# class Article(models.Model):
#     author = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=u'作者')
#     category = models.ForeignKey(Category,verbose_name=u'分类')
#     title = models.CharField(max_length=100,verbose_name=u'标题')
#     en_title = models.CharField(max_length=100,verbose_name=u'英文标题')
#     img = models.CharField(max_length=200,default='/static/img/article/default.jpg')
#     tags = models.CharField(max_length=200,null=True,blank=True,verbose_name=u'标签',help_text=u'用逗号分隔')
#     summary = models.TextField(verbose_name=u'摘要')
#     content = models.TextField(verbose_name=u'正文')
#
#     view_times = models.IntegerField(default=0)
#     zan_times = models.IntegerField(default=0)
#
#     is_top = models.BooleanField(default=False,verbose_name=u'置顶')
#     rank = models.IntegerField(default=0,verbose_name=u'排序')
#     status = models.IntegerField(default=0,choices=STATUS.items(),verbose_name='状态')
#
#
#     pub_time = models.DateTimeField(default=False,verbose_name=u'发布时间')
#     create_time = models.DateTimeField(u'创建时间',auto_now_add=True)
#     update_time = models.DateTimeField(u'更新时间',auto_now=True)
#
#     def get_tags(self):
#         return self.tags.split(',')
#
#     class Meta:
#         verbose_name_plural = verbose_name = u'文章'
#         ordering = ['rank','-is_top','-pub_time','-create_time']
#         app_label = string_with_title('blog',u"内容管理")
#
#     def __unicode__(self):
#             return self.title

class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=u'发布者',null=True,blank=True)
    category = models.ForeignKey(Category,verbose_name=u'分类')
    title = models.CharField(max_length=100,verbose_name=u'标题')
    en_title = models.CharField(max_length=100,verbose_name=u'影片编码',unique=True,help_text=u'系统内部标识，不可重复,只能用数字或者字母')
    #add by levy @20150610
    theme = models.CharField(max_length=100,verbose_name=u'题材',null=True,blank=True,help_text=u'用,分隔')
    country = models.CharField(max_length=100,verbose_name=u'国家',null=True,blank=True)
    director = models.CharField(max_length=100,verbose_name=u'导演',null=True,blank=True)
    actor = models.CharField(max_length=200,null=True,blank=True,verbose_name=u'演员',help_text=u'用,分隔')

    #img = models.CharField(max_length=200,default='/static/img/article/default.jpg')
    img = models.FileField(upload_to='./static/upload/',null=True,blank=True)
    vod = models.FileField(upload_to='./static/video/',null=True,blank=True)
    tags = models.CharField(max_length=200,null=True,blank=True,verbose_name=u'标签',help_text=u'用,分隔')
    summary = models.TextField(verbose_name=u'摘要')
    content = models.TextField(verbose_name=u'内容')



    view_times = models.IntegerField(default=0)
    zan_times = models.IntegerField(default=0)

    is_top = models.BooleanField(default=False,verbose_name=u'猜你喜欢')
    rank = models.IntegerField(default=0,verbose_name=u'排序')
    status = models.IntegerField(default=1,choices=STATUS.items(),verbose_name='状态')
    chgstatus = models.IntegerField(default=1,choices=CHGSTATUS.items(),verbose_name='转码状态')


    pub_time = models.DateTimeField(default=False,verbose_name=u'发布时间')
    create_time = models.DateTimeField(u'创建时间',auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间',auto_now=True)

    def get_tags(self):
        return self.tags.split(',')

    class Meta:
        verbose_name_plural = verbose_name = u'影片'
        ordering = ['rank','-is_top','-pub_time','-create_time']
        app_label = string_with_title('blog',u"1->媒体资源管理")

    def __unicode__(self):
            return self.title

# add by levy @20150625
class Price(models.Model):
    article = models.OneToOneField(Article,verbose_name=u'影片')
    price = models.FloatField(default=0,verbose_name=u'价格')

    class Meta:
        verbose_name_plural = verbose_name = u'价格'
        ordering = ['article']
        app_label = string_with_title('blog',u"1->媒体资源管理")

    def __unicode__(self):
        return self.article.title

class Bought(models.Model):
    article = models.ForeignKey(Article,verbose_name=u'影片')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=u'用户')
    bought_type = models.CharField(max_length=100,verbose_name=u'购买方式',null=True,blank=True) #单独购买/产品包购买
    bought_time = models.DateTimeField(u'购买时间',auto_now=True)

    class Meta:
        verbose_name_plural = verbose_name = u'影片购买'
        unique_together = (("article", "customer"),)
        # ordering = ['customer']
        app_label = string_with_title('vmaig_auth',u"3->运营支撑")

    def __unicode__(self):
        return self.article.title


class Column(models.Model):
    name = models.CharField(max_length=40,verbose_name=u'专栏内容')
    summary = models.TextField(verbose_name=u'专栏摘要')
    article = models.ManyToManyField(Article,verbose_name=u'文章')
    status = models.IntegerField(default=0,choices=STATUS.items(),verbose_name='状态')
    create_time = models.DateTimeField(u'创建时间',auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = u'专栏'
        ordering = ['-create_time']
        app_label = string_with_title('blog',u"1->媒体资源管理")

    def __unicode__(self):
        return self.name


class Carousel(models.Model):
    title = models.CharField(max_length=100,verbose_name=u'标题')
    summary = models.TextField(blank=True,null=True,verbose_name=u'摘要')
    # img = models.CharField(max_length=200,verbose_name=u'轮播图片',default='/static/img/carousel/default.jpg')
    img = models.FileField(upload_to='./static/upload/',verbose_name=u'轮播图片')
    article = models.ForeignKey(Article,verbose_name=u'影片')
    create_time = models.DateTimeField(u'创建时间',auto_now_add=True)
    class Meta:
        verbose_name_plural = verbose_name = u'首页推荐'
        ordering = ['-create_time']
        app_label = string_with_title('vmaig_auth',u"3->运营支撑")


class News(models.Model):
    title = models.CharField(max_length=100,verbose_name=u'标题')
    summary = models.TextField(verbose_name=u'摘要')
    news_from = models.IntegerField(default=0,choices=NEWS.items(),verbose_name='来源')
    url = models.CharField(max_length=200,verbose_name=u'源地址')

    create_time = models.DateTimeField(u'创建时间',auto_now_add=True)
    pub_time = models.DateTimeField(default=False,verbose_name=u'发布时间')


    class Meta:
        verbose_name_plural = verbose_name = u'资讯管理'
        ordering = ['-title']
        app_label = string_with_title('vmaig_auth',u"3->运营支撑")

    def __unicode__(self):
        return self.title


#add by levy @20150621
class Country(models.Model):
    name = models.CharField(max_length=40,verbose_name=u'名称')
    rank = models.IntegerField(default=0,verbose_name=u'排序')
    status = models.IntegerField(default=0,choices=STATUS.items(),verbose_name='状态')

    create_time = models.DateTimeField(u'创建时间',auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = u'国家'
        ordering = ['rank','-create_time']
        app_label = string_with_title('blog',u"1->媒体资源管理")


    def __unicode__(self):
        return self.name

class Theme(models.Model):
    name = models.CharField(max_length=40,verbose_name=u'名称')
    rank = models.IntegerField(default=0,verbose_name=u'排序')
    status = models.IntegerField(default=0,choices=STATUS.items(),verbose_name='状态')

    create_time = models.DateTimeField(u'创建时间',auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = u'题材'
        ordering = ['rank','-create_time']
        app_label = string_with_title('blog',u"1->媒体资源管理")


    def __unicode__(self):
        return self.name

#add end
