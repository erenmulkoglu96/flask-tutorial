# -*- coding: utf-8 -*-
import os

import psycopg2 as db

def insert(table,columns,values,returnID = True):
	if(returnID==False):
		query = """insert into {} ({}) values({})""".format(table,columns,values)
		run(query)
	else:
		query = """insert into {} ({}) values({}) returning id""".format(table,columns,values)
		return run(query)

def select(columns, table, where=None,asDict=False):
	keywords = []
	if(asDict):
		keywords = columns.replace(' ','').split(',')
	if (where != None):
		query = """select {} from {} where {}""".format(columns, table, where)
	else:
		query = """select {} from {}""".format(columns, table)
	return run(query,keywords)

def update(table, columns, where):
	query = """update {} set {} where {}""".format(table, columns, where)
	run(query)

def delete(table, where):
	query = """delete from {} where {}""".format(table, where)
	run(query)

def run(query, keywords = []):
	connection = None
	cursor = None
	result = None
	print("\nAttempted Query \n", query, "\n--------\n")
	try:
		connection = db.connect(os.getenv("DATABASE_URL"))
		cursor = connection.cursor()
		cursor.execute(query)
		if(not 'drop' in query and not 'update' in query and not 'delete' in query):
			result = cursor.fetchall()
	except db.DatabaseError as dberror:
		if connection != None:
			connection.rollback()
		result = dberror
		print("Error:::", result)
	finally:
		if connection != None:
			connection.commit()
			connection.close()
		if cursor != None:
			cursor.close()
		if(keywords != []):
			final_result = [list(i) for i in result]
			result_dict_array = []
			for row in final_result:
				dictionary = {}
				for i,keyword in enumerate(keywords):	
					dictionary[keyword] = row[i]
				result_dict_array.append(dictionary)
			#print("\nResult of the dict query\n", result_dict_array, "\n",len(result_dict_array),"\n")
			if(len(result_dict_array) == 1):
				return result_dict_array[0]
			return result_dict_array
		#print("\nResult of the list query\n", result, "\n")
		return result