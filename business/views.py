#coding:utf-8
from django import template
from django import forms
from django.http import HttpResponse,Http404
from django.shortcuts import render,render_to_response
from django.template import Context,loader
from django.views.generic import View,TemplateView,ListView,DetailView
from django.db.models import Q
from django.core.cache import caches
from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.contrib.auth.tokens import default_token_generator
from django.utils.timezone import now, timedelta
from blog.models import Article
from vmaig_auth.models import VmaigUser, BuyLog, OprLog
from vmaig_blog.settings import PAGE_NUM
from business.models import FilmPack,PackContent,BoughtPack
from blog.models import Nav,Bought
from vmaig_comments.models import Comment
import datetime,time
import json
import logging

#缓存
try:
    cache = caches['memcache']
except ImportError as e:
    cache = caches['default']

#logger
logger = logging.getLogger(__name__)


class BaseMixin(object):
    
    def get_context_data(self,*args,**kwargs):
        context = super(BaseMixin,self).get_context_data(**kwargs)
        # try:
        #     #热门文章
        #     context['hot_article_list'] = Article.objects.order_by("-view_times")[0:10]
        #     #导航条
        #     context['nav_list'] =  Nav.objects.filter(status=0)
        #     #最新评论
        #     context['latest_comment_list'] = Comment.objects.order_by("-create_time")[0:10]
        #
        # except Exception as e:
        #     logger.error(u'[BaseMixin]加载基本信息出错')

        return context


# class IndexView(BaseMixin,ListView):
#     template_name = 'blog/index.html'
#     context_object_name = 'category_list'
#     paginate_by = PAGE_NUM #分页--每页的数目
#
#     def get_context_data(self,**kwargs):
#         #轮播
#         kwargs['carousel_page_list'] = Carousel.objects.all()
#         kwargs['PAGE_NUM'] = PAGE_NUM
#         return super(IndexView,self).get_context_data(**kwargs)
#
#         # def get_queryset(self):
#         #     article_list = Article.objects.filter(status=0)
#         #     return article_list
#
#     def get_queryset(self):
#         category_list = Category.objects.filter(status = 0)
#         return category_list

class FilmPackView(BaseMixin,ListView):
    template_name = 'business/productpack.html'
    context_object_name = 'article_list'

    def get_context_data(self,**kwargs):
        user = self.request.user
        name = FilmPack.objects.filter(Q(status=0)).all()
        # print len(name)
        if len(name)  == 0:
            kwargs['PackinfoFlag'] = 0
            return super(FilmPackView,self).get_context_data(**kwargs)
        name = name[0]
        # print en_name
        try:
            filmpackcount = PackContent.objects.filter(name = name).count()
            packdesc = FilmPack.objects.get(name = name).summary
            packpri = FilmPack.objects.get(name = name).price
        except FilmPack.DoesNotExist:
            logger.error(u'[AllView_new]此产品包不存在:Category[%s]'  %name)
            raise PermissionDenied

        try:
            Filmbought = BoughtPack.objects.get(name=name, customer_id = user.id)
            PackboughtFlag = True
        except BoughtPack.DoesNotExist:
            PackboughtFlag = False

        kwargs['PackboughtFlag'] = PackboughtFlag
        kwargs['filmpack_list'] = FilmPack.objects.filter(Q(status=0)).all()
        kwargs['filmpackcount'] = filmpackcount
        kwargs['packdesc'] = packdesc
        kwargs['packpri'] = packpri
        kwargs['PAGE_NUM'] = PAGE_NUM
        return super(FilmPackView,self).get_context_data(**kwargs)

    def get_queryset(self):
        article_list = []
        #获取第一个产品包的标识，用于页面load后自动显示默认的页面
        try:
            en_name = FilmPack.objects.filter(Q(status=0)).all()
            if len(en_name) == 0:
                return
            en_name = en_name[0]
            content_list = PackContent.objects.filter(name = en_name)
            #将PackContent表中的数据映射到article表中
            for content in content_list:
                if content.article.status == 0:
                    article_list.append(content.article)
        except FilmPack.DoesNotExist:
            logger.error(u'[AllView_new]此产品包不存在:Category[%s]'  %en_name)
            raise PermissionDenied

        article_list = article_list[0:PAGE_NUM]
        return article_list

    def post(self, request, *args, **kwargs):
        errors = []
        user = self.request.user
        val = self.request.POST.get("val","")
        start = self.request.POST.get("start",0)
        end = self.request.POST.get("end",PAGE_NUM)
        funcval = self.request.POST.get("funcval","")
        article_list = []
        start = int(start)
        end = int(end)
        # print val
        try:
            packid = FilmPack.objects.get(name = val).id
            packdesc = FilmPack.objects.get(id=packid).summary
            packpri = FilmPack.objects.get(id=packid).price
            # print en_name
            content_list = PackContent.objects.filter(name = packid)
            for content in content_list:
                if content.article.status == 0:
                    article_list.append(content.article)

        except PackContent.DoesNotExist:
            logger.error(u'[AllView_new]此产品包不存在:Category[%s]'  %val)
            raise PermissionDenied
        isend = len(article_list) != (end-start+1)
        articlecount = len(article_list)

        #如果点击了购买产品包button
        if funcval == "buypack":
            start = 0
            end = PAGE_NUM
            if not request.user.is_authenticated():
                logger.error(u'[UserControl]用户未登陆')
                raise PermissionDenied
            bought = BoughtPack.objects.create(
                name = FilmPack.objects.get(id=packid),
                customer = self.request.user
            )

            buylog = BuyLog.objects.create(
                name = val,
                customer = request.user,
                buy_type = '产品包',
                price = FilmPack.objects.get(name = val).price,
            )
            #记录日志
            oprlog = OprLog.objects.create(
                name = 'BuyLog',
                customer = self.request.user,
                opr_type = '创建',
                bak = '添加产品包购买记录'
            )
            for article in article_list:
                try:
                    # article_id = Article.objects.get()
                    Filmbought = Bought.objects.get(article=article.id, customer = user.id)
                    # print Filmbought
                except Bought.DoesNotExist:
                    bought = Bought.objects.create(
                        article = article,
                        customer = user,
                        bought_type = val
                    )
                    #记录日志
                    oprlog = OprLog.objects.create(
                        name = 'Bought',
                        customer = self.request.user,
                        opr_type = '创建',
                        bak = '购买产品包，在影片表里添加记录'
                    )
                    # FilmboughtFlag = False

            # 更新用户账户金额
            request.user.useracnt = self.request.POST.get("userbought","")
            request.user.save()
            oprlog = OprLog.objects.create(
                name = 'Bought',
                customer = self.request.user,
                opr_type = '修改',
                bak = '修改账户余额'
            )
        #判断该包是否已经购买
        try:
            Filmbought = BoughtPack.objects.get(name = packid, customer_id = user.id)
            PackboughtFlag = True
        except BoughtPack.DoesNotExist:
            PackboughtFlag = False

        # print start,end

        article_list = article_list[start:end]

        html = ""
        for article in article_list:
            html +=  template.loader.get_template('business/include/all_post.html').render(template.Context({'post':article}))
        mydict = {"html":html,"isend":isend,"packcount":articlecount,
                  "packdesc":packdesc,"packpri":packpri,"errors":errors,
                  "filmpack":val,"PackboughtFlag":PackboughtFlag}
        return HttpResponse(json.dumps(mydict),content_type="application/json")

