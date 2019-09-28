from django.http import HttpResponse, JsonResponse

def numbers(request):
	number = request.GET['list']
	number = sorted([int(n) for n in sorted(number.split(','))])

	data = {'response': 'ok',
	'data':number}

	return JsonResponse(data)