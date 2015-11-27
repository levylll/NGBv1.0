#coding:utf-8
import xadmin
from blog.models import Article,Category,Carousel,Nav,Column,News,Country,Theme,Price,Bought
from xadmin.layout import Main, Fieldset


class CategoryAdmin(object):
    search_fields = ('name',)
    list_filter = ('status','create_time')
    list_display = ('name','parent','rank','status')
    fields = ('name','parent','rank','status')



class ArticleAdmin(object):
    search_fields = ('title','summary')
    list_filter = ('status','category','is_top','create_time','update_time')
    list_display = ('title','is_top','category','author','status','update_time','chgstatus')
    # fieldsets = (
    #     (u'基本信息', {
    #         'fields': ('title','en_title','is_top','img','category','tags','author','rank','status')
    #         }),
    #     (u'内容', {
    #         'fields': ('content',)
    #         }),
    #     (u'摘要', {
    #         'fields': ('summary',)
    #         }),
    #     (u'时间', {
    #         'fields': ('pub_time',)
    #         }),
    # )

    form_layout = (
        Fieldset(u'基本信息',
                 'title','en_title','img','vod','category','author','director','actor','country','theme','is_top','status','chgstatus'
                 ),
        Fieldset(u'摘要',
                 'summary'
                 ),
        Fieldset(u'内容',
                 'content'
                 ),
        Fieldset(u'时间',
                 'pub_time'
                 )
    )

    def get_readonly_fields( request,obj=None):
        fields=[]
        fields = ['chgstatus']
        if request.user.is_superuser:
            return fields
        else:
            # fields=['status']
            fields.append('status')
            return fields
    #
    # def get_readonly_fields(self, request, obj=None):
    #     if request.user.is_superuser:
    #         return super(ArticleAdmin, self).get_readonly_fields(request, obj)
    #     else:
    #         return ('status')
    # fieldsets = [
    #     (u'基本信息', {'fields': ('title','en_title','is_top','img','category','tags','author','rank','status')}),
    #     (u'内容', { 'fields': ('content',)}),
    #     (u'摘要', { 'fields': ('summary',)}),
    #     (u'时间', {'fields': ('pub_time',)}),
    #     ]

class PriceAdmin(object):
    search_fields = ('article')
    list_filter = ('article','price')
    list_display = ('article','price')

class BoughtAdmin(object):
    search_fields = ('article','customer')
    list_filter = ('article','customer','bought_time')
    list_display = ('article','customer','bought_time')


class NewsAdmin(object):
    search_fields = ('title','summary')
    list_filter = ('news_from','create_time')
    list_display = ('title','news_from','url','create_time')
    fields = ('title','news_from','url','summary','pub_time')


# class NavAdmin(object):
#     search_fields = ('name',)
#     list_display = ('name','url','status','create_time')
#     list_filter = ('status','create_time')
#     fields = ('name','url','status')


# class ColumnAdmin(object):
#     search_fields = ('name',)
#     list_display = ('name','status','create_time')
#     list_filter = ('status','create_time')
#     fields = ('name','status','article','summary')
#     filter_horizontal = ('article',)


class CarouselAdmin(object):
    search_fields = ('title',)
    list_display = ('title','article','img','create_time')
    list_filter = ('create_time',)
    fields = ('title','article','img','summary')


#add by levy @20150621
class CountryAdmin(object):
    search_fields = ('name',)
    list_filter = ('status','create_time')
    list_display = ('name','rank','status')
    fields = ('name','rank','status')

class ThemeAdmin(object):
    search_fields = ('name',)
    list_filter = ('status','create_time')
    list_display = ('name','rank','status')
    fields = ('name','rank','status')
#add end


class GlobalSetting(object):
    site_title = u"业务门户仿真系统"
    site_footer = u"业务门户仿真系统"


class MainDashboard(object):
    widgets = [
        [
            {"type": "html", "title": "欢迎",
            "content": "<h3> Welcome to Vmaig! </h3>\
                        <p>欢迎来到 levyDEMO ,如果有任何问题可以加:<br/>\
                        我的QQ：348878516<br/>\
                        首页的便签云中的内容，在后台不能修改。 请修改 blog/templates/blog/widgets/tags_cloud.html 中的 tags数组的内容。<br/><br/>"},
        ],
    ]


xadmin.site.register(xadmin.views.CommAdminView,GlobalSetting)
xadmin.site.register(xadmin.views.website.IndexView, MainDashboard)

xadmin.site.register(Category,CategoryAdmin)
xadmin.site.register(Country,CountryAdmin)
xadmin.site.register(Theme,ThemeAdmin)
xadmin.site.register(Article,ArticleAdmin)
xadmin.site.register(Price,PriceAdmin)

# xadmin.site.register(Nav,NavAdmin)
# xadmin.site.register(Column,ColumnAdmin)
xadmin.site.register(Carousel,CarouselAdmin)
xadmin.site.register(Bought,BoughtAdmin)

xadmin.site.register(News,NewsAdmin)


