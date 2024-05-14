from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from globa.moysklad import Moysklad


@csrf_exempt
def webhook(request):
    print(request.body)
    if request.method == 'POST':
        print(request.body)
        retaildemang_id = request.body['events'][0]['meta']['href'].split('/')[-1]
        ms = Moysklad()
        ms.edit_retaildemand_description(retaildemang_id)
        print(f'Edited {retaildemang_id}')
        return JsonResponse({'status': 'ok'})
    if request.method == 'GET':
        print(request.GET)
        return JsonResponse({'status': 'ok'})
