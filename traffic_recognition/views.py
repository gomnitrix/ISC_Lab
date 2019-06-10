from django.shortcuts import render
from django.http import JsonResponse
from identify.main import *
from utils.DbHelper import *


# Create your views here.
def get_html(request):
    DbHelper.delete()
    DbHelper.set_auto()
    return render(request, "index.html", locals())


def start(request):
    ident.message_share()
    data = {"info": "start success"}
    return JsonResponse(data)


def stop(request):
    ident.stop()
    db_close()
    data = {"info": "stop success"}
    return JsonResponse(data)


def proto_num(reguest):
    data = list(get_proto_static().values())
    nums = {"data": data[0:6]}
    return JsonResponse(nums)


def pkt_sum(request):
    data = {"num": get_sum()}
    return JsonResponse(data)


def get_riskflow(request):
    data = {"num": get_riskflow_num()}
    return JsonResponse(data)


def get_rst(request):
    data = {"num": get_rst_num()}
    return JsonResponse(data)


def app_num(request):
    data = list(get_app_num().values())
    nums = {"num": data[0:6]}
    return JsonResponse(nums)


def riskflow_dtl(request):
    data = {}
    values = get_riskflow_retail()
    print(values)
    if len(values) == 0:
        data["data"] = 0
        return JsonResponse(data)
    data["data"] = values
    return JsonResponse(data)
