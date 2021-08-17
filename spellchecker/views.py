from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def checker(request):

    if request.method == 'POST':
        return JsonResponse({"status": "OK", "message": "POST"})
    else:
        return JsonResponse({"status": "OK", "message": "GET"})

