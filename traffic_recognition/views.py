from django.shortcuts import render
from django.http import JsonResponse
from identify import main
# Create your views here.
def get_html(request):
    return render(request, "index.html", locals())
def start(request):
    main.message_share()
    data = {}
    data["info"] = "start success"
    return JsonResponse(data)

def stop(request):
    main.stop()
    data = {}
    data["info"] = "stop success"
    return JsonResponse(data)

def proto_num(reguest):
    data = list(main.get_static().values())
    print(data)
    nums ={}
    nums["data"] = data[0:6]
    return JsonResponse(nums)

def get_sum(request):
    data = {}
    data["num"] = main.get_sum()
    return JsonResponse(data)
def get_riskflow(request):
    data = {}
    data["num"] = main.get_riskflow_num()
    return  JsonResponse(data)
def get_rst(request):
    data = {}
    data["num"] = main.get_rst_num()
    return JsonResponse(data)