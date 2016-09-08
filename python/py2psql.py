#
# author : jiankaiwang (http://jiankaiwang.no-ip.biz/)
# source code in github : seed (https://github.com/jiankaiwang/seed)
# document in gitbook : seed (https://www.gitbook.com/book/jiankaiwang/seed/details)
#

#
# example :
#
# link to postgresql database
# p2l = py2psql("127.0.0.1","5432","ckan_default","public.user","ckan_default","ckan")
#
# query data and select column name, email, 123 (not existing)
# data = p2l.select({"name":"test114"},["name","email","123"])
# data = p2l.select({"name":"test114"},[])
#
# query data and select column name, email, 123 (not existing) and also returned as dictionary
# data = p2l.select({"name":"test114"},["name","email","123"],asdict=True)
# data = p2l.select({"name":"test114"},[],asdict=True)
#
# update data
# p2l.update({"email":"test@tw"},{"name":"test114"})
#
# insert data
# p2l.insert({ "id" : "acbdhcbdh-abchdbch", "name":"123","email":"123@tw" })
#
# delete data
# p2l.delete({"name":"test1", "email":"test1@tw"})
#

import psycopg2

class py2psql:
	
	# private member
	# host : URL or IP
	# port : postgresql server port
	# db : as a string
	# tb : as a string
	# user : as a string
	# pwd : as a string
	# data : as a dictionary, { colName : colValue }
	# columns : save table schema
	# datatype : save column data tpye { "col" : { "type" : "code", "null" : "True/False" } }
	__host = ""
	__port = ""
	__db = ""
	__tb = ""
	__user = ""
	__pwd = ""
	__columns = []
	__datatype = {}

	# constructor
	def __init__(self, getHost, getPort, getDB, getTB, getUser, getPwd):
		self.__host = getHost
		self.__port = getPort
		self.__db = getDB
		self.__tb = getTB
		self.__user = getUser
		self.__pwd = getPwd
		self.__columns = []
		self.__datatype = {}

		# fetch column information
		self.__tableSchema()
			
	# define server DSN
	def __serverDSN(self):
		conStr = ["host=" + self.__host, "port=" + self.__port, "dbname=" + self.__db, "user=" + self.__user , "password=" + self.__pwd]
		return ' '.join(conStr)

	# get table schema
	def __tableSchema(self):
		# Connect to an existing database
		conn = psycopg2.connect(self.__serverDSN())
		
		# Open a cursor to perform database operations
		cur = conn.cursor()

		# select sql
		selectStr = "select * from " + self.__tb

		cur.execute(selectStr)
		
		# get columns
		self.__columns = [desc[0] for desc in cur.description]

		# close communication
		cur.close()
		conn.close()

	# get table colunm data type
	def __tableColDatatype(self):
		# Connect to an existing database
		conn = psycopg2.connect(self.__serverDSN())
		
		# Open a cursor to perform database operations
		cur = conn.cursor()

		# select sql
		selectStr = "select * from " + self.__tb

		cur.execute(selectStr)
		
		# get column data type
		for item in cur.description:
			self.__datatype.setdefault(item[0], { "type" : item[1] , "null" : item[6] })
		
		# close communication
		cur.close()
		conn.close()

		return self.__datatype
		
		
	# get col index in the column order
	def __getColIndex(self, getColName):
		if getColName in self.__columns:
			return self.__columns.index(getColName)
		else:
			return -1
		
	# select operation
	# getConds{} : defined where SQL conditions
	# getParams [] : selected column names, empty : means all
	# asdict : returned row as dictionary data type
	def select(self, getConds, getParams, asdict=False):
		# filter the column value
		colSelected = "*"
		colList = []
		retdata = []
		dataTuple = ()
		
		# check column existing
		if len(getParams) > 0:
			for item in getParams:		
				if self.__getColIndex(item) > -1:
					colList.append(item)
		
		# set selected columns
		if len(colList) > 0:
			colSelected = ','.join(colList)
								
		# Connect to an existing database
		conn = psycopg2.connect(self.__serverDSN())
		
		# Open a cursor to perform database operations
		cur = conn.cursor()

		# select sql
		selectStr = "select " + colSelected + " from " + self.__tb

		if len(getConds.keys()) > 0:
			selectStr += " where "
			item = 0
			for key, value in getConds.iteritems():
				if item != 0:
					selectStr += " and "
				selectStr += str(key) + "= %s "
				item += 1
				dataTuple += (value,)
		selectStr += ";"												

		# parameter-based select sql
		cur.execute(selectStr, dataTuple)

		# get all data	
		rawdata = cur.fetchall()
		
		# modify data to customized type
		if asdict:
			if len(colList) > 0:
				for pair in rawdata:
					tmpDict = {}
					for item in range(0,len(pair),1):
						tmpDict.setdefault(colList[item],pair[item])
					retdata.append(tmpDict)
			else:
				for pair in rawdata:
					tmpDict = {}
					for item in range(0,len(pair),1):
						tmpDict.setdefault(self.__columns[item],pair[item])
					retdata.append(tmpDict)
		else:
			retdata = rawdata

		# close communication
		cur.close()
		conn.close()											 

		return retdata

	# update operation
	# getParams : {}, set sql parameters	
	# getConds : {}, where sql conditions
	def update(self, getParams, getConds):
		# 0 : failure, 1 : success
		retStatus = 1
	
		# filter the column value
		paraKeys = getParams.keys()
		condKeys = getConds.keys()
		paraList = []
		condList = []
		dataTuple = ()
		
		# check parameter existing
		if len(paraKeys) > 0:
			for item in paraKeys:	 
				if self.__getColIndex(item) > -1:
					paraList.append(item)
		else:
			return retStatus
		
		# check condition existing
		if len(condKeys) > 0:
			for item in condKeys:	 
				if self.__getColIndex(item) > -1:
					condList.append(item)
		else:
			return retStatus

		# update sql
		updateStr = "update " + self.__tb + " set "
		
		if len(paraList) > 0:
			paraListItem = []
			for item in paraList:
				paraListItem.append(item + "= %s ")
			updateStr += ' , '.join(paraListItem)
			dataTuple += (getParams[item],)
		else:
			return retStatus
			
		updateStr += " where "

		if len(condList) > 0:
			condListItem = []
			for item in condList:
				condListItem.append(item + "= %s ")
			updateStr += ' and '.join(condListItem)
			dataTuple += (getConds[item],)
		else:
			return retStatus
		
		updateStr += ";"					 

		# Connect to an existing database
		conn = psycopg2.connect(self.__serverDSN())
		
		# Open a cursor to perform database operations
		cur = conn.cursor()	 

		# parameter-based update sql
		cur.execute(updateStr, dataTuple)

		# get all data	
		conn.commit()

		# close communication
		cur.close()
		conn.close()											 

		return retStatus		
		
	# insert operation
	# getParams : {}, value sql parameters	
	def insert(self, getParams):
		# 0 : failure, 1 : success
		retStatus = 1
	
		# filter the column value
		paraKeys = getParams.keys()
		paraList = []
		insertedData = ()
		
		# check parameter existing
		if len(paraKeys) > 0:
			for item in paraKeys:	 
				if self.__getColIndex(item) > -1:
					paraList.append(item)
		else:
			return retStatus
			
		# insert string
		insertStr = "insert into " + self.__tb + " ("
		
		for index in range(0,len(paraList),1):
			if index != 0:
				insertStr += ', '
			insertStr += paraList[index]
		
		insertStr += ') values ('
		
		for index in range(0,len(paraList),1):
			if index != 0:
				insertStr += ', '
			insertStr += "%s"
			insertedData += (getParams[paraList[index]],)
		
		insertStr += ')'
		
		try:
		
			# Connect to an existing database
			conn = psycopg2.connect(self.__serverDSN())
			
			# Open a cursor to perform database operations
			cur = conn.cursor()	 

			# parameter-based insertion sql
			cur.execute(insertStr,insertedData)

			# get all data	
			conn.commit()

			# close communication
			cur.close()
			conn.close()
		
		except:
			retStatus = 0
		
		return retStatus

	# delete operation
	# getConds : {}, where sql conditions
	def delete(self, getConds):
		# 0 : failure, 1 : success
		retStatus = 1
	
		# filter the column value
		condKeys = getConds.keys()
		condList = []
		selectedTuple = ()
		
		# check parameter existing
		if len(condKeys) > 0:
			for item in condKeys:	 
				if self.__getColIndex(item) > -1:
					condList.append(item)
		else:
			return retStatus

		# no where condition
		if len(condList) < 1:
			return retStatus
			
		# delete string
		deleteStr = "delete from " + self.__tb + " where "
		
		for index in range(0,len(condList),1):
			if index != 0:
				deleteStr += ' and '
			deleteStr += condList[index] + " = " + "%s"
			selectedTuple += (getConds[condList[index]],)
            
		# delete transaction
		try:
		
			# Connect to an existing database
			conn = psycopg2.connect(self.__serverDSN())
			
			# Open a cursor to perform database operations
			cur = conn.cursor()	 

			# parameter-based sql
			cur.execute(deleteStr, selectedTuple)

			# get all data	
			conn.commit()

			# close communication
			cur.close()
			conn.close()
		
		except:
			retStatus = 0
		
		return retStatus
		
	
	
	
	
	
	
	
	
	
	
	
	
	
