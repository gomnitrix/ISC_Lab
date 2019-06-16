from django.http import JsonResponse
from django.shortcuts import render

from identify.main import *
from catch_package.catch_pkt import FLT
from utils.DbHelper import *


# Create your views here.
def get_setting(request):
    values = get_filter()
    print(values)
    return render(request, "inputs.html", {"outs": values}, locals())


def get_html(request):
    DbHelper.delete()
    DbHelper.set_auto()
    return render(request, "index.html", locals())


def start(request):
    # iptable_enable()
    ident.message_share()
    data = {"info": "start success"}
    return JsonResponse(data)


def stop(request):
    ident.stop()
    # iptable_reset()
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


def get_block(request):
    data = {"num": get_block_num()}
    return JsonResponse(data)


def get_rst(request):
    data = {"num": get_rst_num()}
    return JsonResponse(data)


def app_num(request):
    data = list(get_app_num().values())
    nums = {"num": data[0:6]}
    return JsonResponse(nums)


def filter(request):
    ft = request.GET.get("ft")
    FLT.append(ft)
    write_ft(ft)
    data = {}
    data["data"] = "s"
    return JsonResponse(data)


def filter_delete(request):
    ft = request.GET.get("ft")
    delete_flt(ft)
    data = {}
    data["data"] = "s"
    print(data["data"])
    return JsonResponse(data)


def riskflow_dtl(request):
    data = {}
    values = get_riskflow_retail()
    if len(values) == 0:
        data["data"] = 0
        return JsonResponse(data)
    data["data"] = values
    return JsonResponse(data)
