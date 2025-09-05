from django.shortcuts import render,HttpResponse

# Create your views here.
def key_logger(request):
    print(request.body)
    return HttpResponse("KeyLogger")