from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from globa.moysklad import Moysklad
import json

init = Moysklad()
init = None


@csrf_exempt
def webhook(request):
    print(request.body)
    if request.method == 'POST':
        body = json.loads(request.body)
        action_type = body['events'][0]['action']
        if action_type == 'CREATE':
            print('CREATE')
            retaildemang_id = body['events'][0]['meta']['href'].split('/')[-1]
            ms = Moysklad()
            ms.edit_retaildemand_description(retaildemang_id)
            print(f'Edited {retaildemang_id}')
            return JsonResponse({'status': 'ok'})
        elif action_type == 'UPDATE':
            print('UPDATE')
            retaildemang_id = body['events'][0]['meta']['href'].split('/')[-1]
            ms = Moysklad()
            ms.edit_retaildemand_description(retaildemang_id)
            print(f'Edited {retaildemang_id}')
            return JsonResponse({'status': 'ok'})
    if request.method == 'GET':
        print(request.GET)
        return JsonResponse({'status': 'ok'})
