from smartcard.System import readers
import sys, time

def get_id(message = None):
	r = readers()
	
	if len(r) == 0: return None
	
	reader = r[0]
	
	if message is not None: print(message)
	
	while True:
		try:
			connection = reader.createConnection()
			
			status_connection = connection.connect()
			resp = connection.transmit([0xFF, 0xCA, 0x00, 0x00, 0x00])
			
			l = len(resp[0])
			
			if l < 2: return None
			
			tag_id = 0
			
			for i in range(l):
				try: number = int(resp[0][i])
				except: return None
				
				tag_id += number ** (l - i)
			
			return tag_id
		
		except Exception as e:
			continue
	
	return None
