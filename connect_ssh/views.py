#from django.shortcuts import render
import paramiko

class Conection_ssh():
	"""create a client for Conection_ssh"""

	def __init__(self, ip='192.168.190.3', port='22', username='vagrant', password='vagrant', command = 'cat /edx/var/log/tracking/tracking.log'):
		
		self.ip = ip
		self.port = port
		self.username = username
		self.password = password
		self.command = command

	def connect(self):

		print("creating ssh client...")
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.load_system_host_keys()

		print("connecting with remote server")
		client.connect(self.ip, self.port, self.username, self.password)

		print("executing command")
		stdin, stdout, stderr = client.exec_command(self.command)

		stdout = stdout.readlines()
		print("closing connection")
		client.close()

		print("return output..")		

		return stdout