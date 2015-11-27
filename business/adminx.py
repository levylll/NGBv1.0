#coding:utf-8
import xadmin
from business.models import FilmPack,PackContent,BoughtPack


class FilmPackAdmin(object):
    search_fields = ('name','en_name',)
    list_filter = ('status','create_time')
    list_display = ('name','en_name','price','rank','status','create_time')
    fields = ('name','en_name','price','rank','status','summary')

class PackContentAdmin(object):
    search_fields = ('name',)
    list_filter = ('name','create_time')
    list_display = ('name','article','create_time')
    fields = ('name','article')

class BoughtPackAdmin(object):
    search_fields = ('name','customer')
    list_filter = ('name','customer','bought_time')
    list_display = ('name','customer','bought_time')

xadmin.site.register(FilmPack,FilmPackAdmin)
xadmin.site.register(PackContent,PackContentAdmin)
xadmin.site.register(BoughtPack,BoughtPackAdmin)
