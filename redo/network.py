import socket


class Network:
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.settimeout(0.1)
		self.server = "192.168.0.14"
		self.port = 9999
		self.format = "utf-8"
		self.client.connect((self.server, self.port))




	def send(self, msg):
		try:
			message = msg.encode(self.format)

			self.client.send(message)
			message = self.client.recv(2048).decode(self.format)
			return message
		except socket.error as e:
			print(e)