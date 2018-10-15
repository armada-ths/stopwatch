#!/usr/bin/python3

import mysql.connector
import config
import sys
import NFC
import threading
import socket


gotten = []


def send_id(id):
	id = str(id).zfill(16)
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((config.SERVER_HOST, config.SERVER_PORT))
	
	s.send(id.encode('utf-8'))
	s.close()


while True:
	print('ready')
	id = NFC.get_id()
	
	if id is not None and id not in gotten:
		print(id)
		gotten.append(id)
		
		thread = threading.Thread(target = send_id, args = [id])
		thread.daemon = True
		thread.start()
