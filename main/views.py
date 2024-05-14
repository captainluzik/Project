from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def webhook(request):
    print(request.body)
    if request.method == 'POST':
        print(request.body)
        return JsonResponse({'status': 'ok'})
    if request.method == 'GET':
        print(request.GET)
        return JsonResponse({'status': 'ok'})
