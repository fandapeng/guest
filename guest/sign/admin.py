from django.contrib import admin
from sign.models import Event,Guest

# Register your models here.
#Django自带admin后台
#把models里面的表映射到后台管理


class EventAdmin(admin.ModelAdmin):
    #将各字段展示在前台
    list_display = ['name','limit','status','address','start_time']
    search_fields = ['name'] #搜索栏
    list_filter = ['status'] #过滤器
class GuestAdmin(admin.ModelAdmin):
    #将各字段展示在前台
    list_display = ['realname','phone','email','sign','event']
    search_fields = ['realname','phone'] #搜索栏
    list_filter = ['sign'] #过滤器

#把models里面的表映射到后台管理
admin.site.register(Event,EventAdmin)
admin.site.register(Guest,GuestAdmin)
