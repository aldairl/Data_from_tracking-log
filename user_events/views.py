from django.shortcuts import render
from connect_ssh import views as conn_ssh
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
	file = open("/home/thinking/ironwood/python_scripts/registry.txt", "rb+")
	info = pickle.load(file)
	file.close()

	#connection to server
	connection = conn_ssh.Conection_ssh(ip="192.168.0.3")
	try:
		stdout = connection.connect()

	except:
		print('Connection Failled')
		print(info[-5])

	else:

		mytime = info[-1]['time']
		print(mytime)

		for n in stdout:

			objson = json.loads(n)

			date = datetime.fromisoformat(objson['time'])

			#.replace(tzinfo=None)
			objson['time'] = datetime.fromisoformat(objson['time'])-delta
		 
			if (date - delta) > mytime:

				info.append(objson)

				print("Ip: {} event: {} time {}".format(objson['ip'], objson['event'], objson['time']))

		file = open("registry.txt", "wb")
		pickle.dump(info, file)
		file.close()

	return render(request, 'data.html', {'data':info[-4:]})



