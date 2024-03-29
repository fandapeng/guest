# -*- coding: utf-8 -*-
__author__ = "dpeng_Fan"

from django.http import JsonResponse
from sign.models import Event,Guest
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import time

def add_event(request):
    if request.method == "POST":
        eid = request.POST.get('eid', '')  # 发布会 id
        name = request.POST.get('name', '')  # 发布会标题
        limit = request.POST.get('limit', '')  # 限制人数
        status = request.POST.get('status', '')  # 状态
        address = request.POST.get('address', '')  # 地址
        start_time = request.POST.get('start_time', '')  # 发布会时间
        if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
            return JsonResponse({'status': 10021, 'message': 'parameter error'})
        result = Event.objects.filter(id=eid)
        if result:
            return JsonResponse({'status': 10022, 'message': 'event id already exists'})
        result = Event.objects.filter(name=name)
        if result:
            return JsonResponse({'status': 10023,
                                 'message': 'event name already exists'})
        if status == '':
            status = 1
        try:
            Event.objects.create(id=eid, name=name, limit=limit, address=address,
                                 status=int(status), start_time=start_time)
        except ValidationError as e:
            error = 'start_time format error. It must be in YYYY-MM-DD HH:MM:SS format.'
            return JsonResponse({'status': 10024, 'message': error})
        return JsonResponse({'status': 200, 'message': 'add event success'})
    else:
        return JsonResponse({"status": 10031, "message": "请求方法错误"})


# 发布会查询接口
def get_event_list(request):
    eid = request.GET.get("eid", "")  # 发布会 id
    name = request.GET.get("name", "")  # 发布会名称
    if eid == '' and name == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})
    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})
        else:
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status': 200, 'message': 'success', 'data': event})
    if name != '':
        datas = []
        results = Event.objects.filter(name__contains=name)
        if results:
            for r in results:
                event = {}
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
            return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
    else:
        return JsonResponse({'status': 10022, 'message': 'query result is empty'})


# 嘉宾签到接口
def user_sign(request):
    eid = request.POST.get('eid', '')  # 发布会 id
    phone = request.POST.get('phone', '')  # 嘉宾手机号
    if eid == '' or phone == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})
    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status': 10022, 'message': 'event id null'})
    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status': 10023,
                             'message': 'event status is not available'})
    event_time = Event.objects.get(id=eid).start_time  # 发布会时间
    etime = str(event_time).split(".")[0]
    timeArray = time.strptime(etime, "%Y-%m-%d %H:%M:%S")
    e_time = int(time.mktime(timeArray))
    now_time = str(time.time())  # 当前时间
    ntime = now_time.split(".")[0]
    n_time = int(ntime)
    if n_time >= e_time:
        return JsonResponse({'status': 10024, 'message': 'event has started'})
    result = Guest.objects.filter(phone=phone)
    if not result:
        return JsonResponse({'status': 10025, 'message': 'user phone null'})
    result = Guest.objects.filter(event_id=eid, phone=phone)
    if not result:
        return JsonResponse({'status': 10026,
                             'message': 'user did not participate in the conference'})
    result = Guest.objects.get(event_id=eid, phone=phone).sign
    if result:
        return JsonResponse({'status': 10027, 'message': 'user has sign in'})
    else:
        Guest.objects.filter(event_id=eid, phone=phone).update(sign='1')
    return JsonResponse({'status': 200, 'message': 'sign success'})
