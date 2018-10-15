#!/usr/bin/python3

import mysql.connector
import config
import sys
import NFC

def insert_tag(id, team_id):
	cnx = mysql.connector.connect(user = config.DB_USERNAME, password = config.DB_PASSWORD, host = config.DB_HOST, database = config.DB_DATABASE)
	
	# prepare a cursor object using cursor() method
	cursor = cnx.cursor()
	
	# Prepare SQL query to INSERT a record into the database.
	sql = "INSERT INTO tags(`id`, `team_id`) VALUES (" + str(id) + ", " + str(team_id) + ") ON DUPLICATE KEY UPDATE `team_id` = " + str(team_id)
	
	try:
		cursor.execute(sql)
		cnx.commit()
		print('tag and team successfully saved')
	
	except Exception as e:
		cnx.rollback()
		print('an error occurred:')
		print(e)
	
	cursor.close()
	cnx.close()


def get_team_id():
	print('enter the tag\'s associated team ID:')
	id = input('> ')
	
	try:
		return int(id)
	
	except:
		print('invalid team ID')
		sys.exit(1)

id = NFC.get_id('scan a tag...')

if id is None:
	print('failed to acquire tag ID')
	sys.exit(1)

print('got tag: ' + str(id))

team_id = get_team_id()

insert_tag(id, team_id)
