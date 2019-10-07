from django.shortcuts import render
from connect_ssh import views as conn_ssh
from django.http import HttpResponse, JsonResponse

#utilities
import pickle
from io import open
import json
from datetime import datetime, timedelta

# Create your views here.

def data(request):

	#variable for local date
	delta = timedelta(hours=5)

	#open file
	file = open("registry.txt", "rb+")
	info = pickle.load(file)
	file.close()

	#connection to server
	connection = conn_ssh.Conection_ssh(ip="192.168.0.3")
	try:
		stdout = connection.connect()

	except:
		print('Connection Failled')
		#print(info[-5])

	else:

		mytime = info[-1]['time']
		
		for n in stdout:

			objson = json.loads(n)

			date = datetime.fromisoformat(objson['time'])

			#.replace(tzinfo=None)
			objson['time'] = datetime.fromisoformat(objson['time'])-delta
		 
			if (date - delta) > mytime:

				info.append(objson)

				#print("Ip: {} event: {} time {}".format(objson['ip'], objson['event'], objson['time']))

		file = open("registry.txt", "wb")
		print("saving changes")
		pickle.dump(info, file)
		file.close()
		#print(info[-1])

	return render(request, 'data.html', {'data':info[-20:]})


def obj(request):

	file = open("registry.txt", "rb+")
	info = pickle.load(file)
	file.close()

	obj = info[-2]

	return JsonResponse(obj)
	#return HttpResponse(obj)





