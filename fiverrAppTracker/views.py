from django.shortcuts import render
from django.http import JsonResponse
from .models import Orders
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def is_order_paid(request,slug:str):
    
    """
    Retrieves client is isPaid or not.
    """
    if request.method == 'GET':
        order = Orders.objects.filter(slug=slug).first()
        return JsonResponse({"Paid":f"{order.isPaid}"}, safe=False)
            

@csrf_exempt
def is_app_blocked(request,slug:str):
    """
    Retrieves if client is isBlocked or not.
    """
    if request.method == 'GET':
        order = Orders.objects.filter(slug=slug).first()
        return JsonResponse({"block":f"{order.isBlocked}"}, safe=False)

@csrf_exempt
def is_client_disconnected(request,slug:str):
    """
    Retrieves all clients where disconnect_connection is True.
    """
    if request.method == 'GET':
        order = Orders.objects.filter(slug=slug).first()
        return JsonResponse({"disconnect":f"{order.disconnect_connection}"}, safe=False)
