#!/usr/bin/python3

import mysql.connector
import config
import sys
import NFC

def insert_tag(id, team_id):
	cnx = mysql.connector.connect(user = config.DB_USERNAME, password = config.DB_PASSWORD, host = config.DB_HOST, database = config.DB_DATABASE)
	
	cursor = cnx.cursor()
	
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

def search_tag(team_id):
	cnx = mysql.connector.connect(user = config.DB_USERNAME, password = config.DB_PASSWORD, host = config.DB_HOST, database = config.DB_DATABASE)
	
	cursor = cnx.cursor()
	
	try:
		cursor.execute("SELECT `teams`.`id`, `teams`.`name` FROM `tags`, `teams` WHERE `tags`.`id` = " + str(id) + " AND `tags`.`team_id` = `teams`.`id` LIMIT 0,1")
		return cursor.fetchone()
	
	except Exception as e:
		return None
	
	cursor.close()
	cnx.close()


def get_team_id():
	print('enter the tag\'s associated team ID:')
	id = input('> ')
	
	try:
		return int(id)
	
	except:
		print('invalid team ID')
		return None

while True:
	print()
	print()
	
	id = NFC.get_id('scan a tag...')
	
	if id is None:
		print('failed to acquire tag ID')
		continue
	
	print('got tag: ' + str(id))
	
	existing_id = search_tag(id)
	
	if existing_id is not None: print('belongs to: ', existing_id)
	
	team_id = get_team_id()
	
	if team_id is None: continue
	
	insert_tag(id, team_id)
