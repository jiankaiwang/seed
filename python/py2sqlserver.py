# -*- coding: utf-8 -*-
"""
#
# author : jiankaiwang (http://welcome-jiankaiwang.rhcloud.com/)
# source code in github : seed (https://github.com/jiankaiwang/seed)
# document in gitbook : seed (https://www.gitbook.com/book/jiankaiwang/seed/details)
#
# Usage

server = 'localhost'
port = 1433
database = 'Example'
username = 'ExampleUser'
password = 'exampleuser'

py2sqlserver = py2SQLServer(server, port, username, password, database)
if py2sqlserver.validateConnection()['state'] == "success":
    print(py2sqlserver.nonQueryBySQLCmd(\
        'insert into dbo.example("attr1", "attr2", "attr3") values(?, ?, ?);', \
        ('data3', 789, '2017-09-15 11:24:00')\
    ))
    print(py2sqlserver.nonQueryBySQLCmd(\
        'delete from dbo.example where attr2 = ?;', \
        (234,)\
    ))
    print(py2sqlserver.nonQueryBySQLCmd(\
        'update dbo.example set attr2 = ? where attr1 = ?;', \
        (100, "data1")\
    ))
    print(py2sqlserver.nonQueryBySQLCmd(\
        'delete from dbo.example where attr1 = ?;', \
        ("data1",)\
    ))
    print(py2sqlserver.queryBySQLcmd("SELECT * from dbo.example;", ()))
    print(py2sqlserver.getColumnNames("SELECT * from dbo.example;", ()))
"""

import pyodbc

class py2SQLServer:
    
    __driver = ""
    __vaild = False
    __msg = ""
    __dsn = ""
    
    def __retStatus(self, state, info, data):
        return {"state" : state, "info" : info, "data" : data}
    
    def __prepareDSN(self, host, port, user, pwd, dbname):
        return 'DRIVER=' + self.__driver + \
            ';SERVER=' + host + \
            ';PORT=' + str(port) + \
            ';DATABASE=' + dbname + \
            ';UID=' + user + \
            ';PWD='+ pwd
    
    def __init__(self, host, port, user, pwd, dbname):     
        
        # initial
        self.__driver = "{ODBC Driver 13 for SQL Server}"
        self.__vaild = False
        self.__msg = ""
        self.__dsn = ""
        
        # try connection
        try:
            cnxn = pyodbc.connect(self.__prepareDSN(host, port, user, pwd, dbname))
            cnxn.close()
            
            self.__vaild = True
            self.__msg = "The connection is validated."
            self.__dsn = self.__prepareDSN(host, port, user, pwd, dbname)
        except:
            self.__vaild = False
            self.__msg = "The connection is lost."
            
    def validateConnection(self):
        if self.__vaild:
            state = "success"
        else:
            state = "failure"
        return self.__retStatus(state, self.__msg, "")
    
    def getColumnNames(self, sqlCmd, SqlParas):
        if self.__vaild:
            try:
                cnxn = pyodbc.connect(self.__dsn)
                cursor = cnxn.cursor()
                cursor.execute(sqlCmd, SqlParas)
                curInfo = [desc[0] for desc in cursor.description]
                cnxn.close()
                return self.__retStatus("success", "The operation to fetch column names is complete.", curInfo)
            except:
                return self.__retStatus("failure", "The operation to fetch column names failed.", "")
        else:
            return self.__retStatus("failure", "The connection is not validated.", "")
        
    def queryBySQLcmd(self, sqlCmd, SqlParas):
        if self.__vaild:
            try:
                cnxn = pyodbc.connect(self.__dsn)
                cursor = cnxn.cursor()
                cursor.execute(sqlCmd, SqlParas)
                dataInRow = cursor.fetchall()
                cnxn.close()
                return self.__retStatus("success", "The query operation is complete.", dataInRow)
            except:
                return self.__retStatus("failure", "The query operation failed.", "")
        else:
            return self.__retStatus("failure", "The connection is not validated.", "")
    
    def nonQueryBySQLCmd(self, sqlCmd, SqlParas):
        if self.__vaild:
            try:
                cnxn = pyodbc.connect(self.__dsn)
                cursor = cnxn.cursor()
                cursor.execute(sqlCmd, SqlParas)
                cursor.commit()
                cnxn.close()
                return self.__retStatus("success", "The nonquery operation is complete.", "")
            except:
                return self.__retStatus("failure", "The nonquery operation failed.", "")
        else:
            return self.__retStatus("failure", "The connection is not validated.", "")






