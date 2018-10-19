#!/usr/bin/python3

import mysql.connector
import config
import threading
import socket
import time

start = None

def receive_id(clientsocket, address):
	stop = time.time()
	duration = round(stop - start, 2)
	
	MSGLEN = 16
	chunks = []
	bytes_recd = 0
	
	try:
		while bytes_recd < MSGLEN:
			chunk = clientsocket.recv(min(MSGLEN - bytes_recd, 2048))
			
			if chunk == b'':
				print(chunks)
				raise RuntimeError('socket connection broken')
			
			chunks.append(chunk)
			bytes_recd = bytes_recd + len(chunk)
		
		id = int((b''.join(chunks)).decode('utf-8').lstrip('0'))
	
	except Exception as e:
		print(e)
		clientsocket.shutdown(socket.SHUT_RDWR)
		clientsocket.close()
	
	clientsocket.shutdown(socket.SHUT_RDWR)
	clientsocket.close()
	
	cnx = mysql.connector.connect(user = config.DB_USERNAME, password = config.DB_PASSWORD, host = config.DB_HOST, database = config.DB_DATABASE)
	
	# prepare a cursor object using cursor() method
	cursor = cnx.cursor()
	
	# Prepare SQL query to INSERT a record into the database.
	sql = "INSERT INTO times(`tag_id`, `timestamp`, `duration`) VALUES (" + str(id) + ", " + str(round(stop)) + ", " + str(duration) + ")"
	
	try:
		cursor.execute(sql)
		cnx.commit()
		print('tag and duration successfully saved')
	
	except Exception as e:
		cnx.rollback()
		print('an error occurred:')
		print(e)
	
	print({
		'id': id,
		'start': start,
		'stop': stop,
		'duration': duration
	})
	
	cursor.close()
	cnx.close()


input('press ENTER key to start the stopwatch ')
start = time.time()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket .setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', config.SERVER_PORT))
serversocket.listen(5)

while True:
	(clientsocket, address) = serversocket.accept()
	
	thread = threading.Thread(target = receive_id, args = [clientsocket, address])
	thread.start()

serversocket.close()
