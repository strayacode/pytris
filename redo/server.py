import socket
import threading
import json



PORT = 9999
SERVER = ""
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)

grids = {}

def handle_client(conn, addr, player):
	print(f"New connection: {addr}")
	connected = True
	while connected:
		msg = conn.recv(2048).decode(FORMAT)
		if msg:
			if msg == DISCONNECT_MSG:
				connected = False

			try:
				data = json.loads(msg)
				grids[str(player)] = data
				if threading.activeCount() - 1 == 2:
					if player == 1:
						reply = json.dumps(grids["2"])
					elif player == 2:
						reply = json.dumps(grids["1"])
					
					conn.send(reply.encode(FORMAT))
			except:
				pass
			
		
			
			

		
	conn.close()





def start():
	server.listen()
	print(f"Server is listening on {SERVER}")
	player_count = 0
	while True:
		if player_count < 2:
			conn, addr = server.accept()
			player_count += 1
			thread = threading.Thread(target=handle_client, args=(conn, addr, player_count))
			thread.start()
			print(f"Active Connections: {threading.activeCount() - 1}")
			
		

		




print("Server is starting...")
start()
