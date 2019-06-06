from django.shortcuts import render
from django.http import JsonResponse
from identify import main
# Create your views here.

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
    return JsonResponse(main.get_static())