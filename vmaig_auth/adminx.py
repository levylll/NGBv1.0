#coding:utf-8
from django.contrib.auth.models import Group,Permission
from django.contrib.auth.admin import UserAdmin
from vmaig_auth.models import VmaigUser,BuyLog,ChargeLog,OprLog
from vmaig_auth.forms import VmaigUserCreationForm
from blog.models import Bought
# add by levy @20150711 for log record module
from django import forms
from django.utils.encoding import force_text
from django.utils.html import format_html

from django_extlog.models import ExtLog
from django_extensions.db.fields.json import JSONField
# add end
import xadmin
from reversion.models import Revision

# Register your models here.

# class VmaigUserAdmin(object):
#     add_form = VmaigUserCreationForm
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username','email' , 'password1', 'password2')}
#         ),
#     )
#     fieldsets = (
#         (u'基本信息', {'fields': ('username', 'password','email')}),
#         (u'权限', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
#         (u'时间信息', {'fields': ('last_login', 'date_joined')}),
#     )

# class BoughtAdmin(object):
#     search_fields = ('article','customer')
#     list_filter = ('article','customer','bought_time')
#     list_display = ('article','customer','bought_time')


class BuyLogAdmin(object):
    search_fields = ('name','customer','buy_type')
    list_filter = ('buy_type','create_time')
    list_display = ('name','customer','buy_type','price','bak','create_time')
    fields = ('bak',)

class ChargeLogAdmin(object):
    search_fields = ('customer',)
    list_filter = ('create_time',)
    list_display = ('customer','money','bak','create_time')
    fields = ('bak',)

class OprLogAdmin(object):
    search_fields = ('customer',)
    list_filter = ('create_time',)
    list_display = ('customer','money','bak','create_time')
    fields = ('bak',)

class OprLogAdmin(object):
    search_fields = ('name','customer','opr_type')
    list_filter = ('opr_type','create_time')
    list_display = ('name','customer','opr_type','bak','create_time')
    fields = ('bak',)

#add  by levy @20150711 for log  record module
class JSONReadonlyTextArea(forms.Textarea):

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        html = u''
        if value:
            for key, item in value[0]['fields'].items():
                html += u'''
                    <strong>{0}</strong>: {1} <br />
                    '''.format(key, force_text(item))
        return format_html(html)



class ExtLogAdmin(object):

    list_filter = [
        'user',
        'action',
        'created_at',
    ]

    date_hierarchy = 'created_at'

    list_display = [
        'created_at',
        'action',
        'get_model_name',
        'object_id',
        'user',
        'ip',
    ]

    search_fields = [
        'object_instance',
        'ip',
    ]

    formfield_overrides = {
        JSONField: {'widget': JSONReadonlyTextArea},
    }

    # def has_delete_permission(self, request, obj=None):
    #     return False
    #
    # def has_add_permission(self, request):
    #     return False
    #
    # def get_actions(self, request):
    #     actions = super(ExtLogAdmin, self).get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions
    #
    # def get_readonly_fields(self, request, obj=None):
    #     # make all fields readonly
    #     readonly_fields = list(set(
    #         [field.name for field in self.opts.local_fields] +
    #         [field.name for field in self.opts.local_many_to_many]
    #     ))
    #     if 'object_instance' in readonly_fields:
    #         readonly_fields.remove('object_instance')
    #     return readonly_fields
    #
    # def formfield_for_dbfield(self, db_field, **kwargs):
    #     if db_field.name == 'object_instance':
    #         kwargs['widget'] = JSONReadonlyTextArea()
    #     return super(ExtLogAdmin, self).formfield_for_dbfield(
    #         db_field,
    #         **kwargs
    #     )

xadmin.site.register(ExtLog, ExtLogAdmin)
#add end


# xadmin.site.register(VmaigUser,VmaigUserAdmin)
# xadmin.site.register(Bought,BoughtAdmin)
xadmin.site.register(BuyLog,BuyLogAdmin)
xadmin.site.register(ChargeLog,ChargeLogAdmin)
xadmin.site.register(OprLog,OprLogAdmin)
xadmin.site.unregister(Group)
xadmin.site.unregister(Permission)
