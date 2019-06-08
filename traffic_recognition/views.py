from django.shortcuts import render
from django.http import JsonResponse
from identify.main import *


# Create your views here.
def get_html(request):
    return render(request, "index.html", locals())


def start(request):
    ident.message_share()
    data = {"info": "start success"}
    return JsonResponse(data)


def stop(request):
    ident.stop()
    data = {"info": "stop success"}
    return JsonResponse(data)


def proto_num(reguest):
    data = list(ident.get_static().values())
    print(data)
    nums = {"data": data[0:6]}
    return JsonResponse(nums)


def get_sum(request):
    data = {"num": get_sum()}
    return JsonResponse(data)


def get_riskflow(request):
    data = {"num": get_riskflow_num()}
    return JsonResponse(data)


def get_rst(request):
    data = {"num": get_rst_num()}
    return JsonResponse(data)
