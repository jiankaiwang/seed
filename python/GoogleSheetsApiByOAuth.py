# -*- coding: utf-8 -*-

"""
#
# author : jiankaiwang (http://welcome-jiankaiwang.rhcloud.com/)
# source code in github : seed (https://github.com/jiankaiwang/seed)
# document in gitbook : seed (https://www.gitbook.com/book/jiankaiwang/seed/details)
#
"""

#
# example.1 : spreadsheets.readonly
# note : the credential must be regenerated
#   |- linux : default /home/(user)/.credentials/sheets.googleapis.com-python-quickstart.json
#   |- windows : default C:\Users\(user)\.credentials\sheets.googleapis.com-python-quickstart.json
#
#fetchDataObj = GoogleSheetsApiByOAuth(\
#                                      "spreadsheets.readonly",\
#                                      "D:\\example\\client_secret.json",\
#                                      "example.1"\
#                                      )
#getStatus = fetchDataObj.fetchData("sheetid", "A:E", 0)

#
# example.2 : spreadsheets (append a new entity as a new raw)
# note : the credential must be regenerated
#
#addDataObj = GoogleSheetsApiByOAuth(\
#                                      "spreadsheets",\
#                                      "D:\\example\\client_secret.json",\
#                                      "example.2"\
#                                      )
#
#getAppendStatus = addDataObj.appendData(\
#                                     "sheetid", \
#                                     [["d2-1", "d2-2", "d2-3", "d2-4","d2-5"]], \
#                                     'RAW', \
#                                     "A:E"
#                                      )
#

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
    
class GoogleSheetsApiByOAuth:

    __SCOPES = ''
    __CLIENT_SECRET_FILE = ''
    __APPLICATION_NAME = ''
    __AvailableCheckState = {}

    #
    # desc : returned status
    # inpt / retn : 
    # |- state : {success|failure}
    # |- info : message
    # |- data : returned data
    #
    def __retState(self, getState, getInfo, getData):
        return { 'state' : getState, 'info' : getInfo, 'data' : getData }

    #
    # desc : get/check the OAuth credential from storage
    # retn : Credentials, the obtained credential.
    # note :
    # |- Use the default credential, "sheets.googleapis.com-python-quickstart.json"
    #
    def __get_credentials(self):
        """   
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-python-quickstart.json')
    
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.__CLIENT_SECRET_FILE, self.__SCOPES)
            flow.user_agent = self.__APPLICATION_NAME
            
            # if there is no credential, google flow would make one in the default directory
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: 
                # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)

        return credentials
        
    #
    # desc : check necessary components
    # inpt : 
    # |- scope, client secret file, app name : refer to constructor
    # retn : None
    # info : self.__AvailableCheckState
    # |- state : {True|False}
    # |- info : message
    #
    def __checkNecessaryComponents(self, getScope, getClientSecretFile, getAppName):
        self.__AvailableCheckState = {'state' : '', 'info' : ''}
        
        # check scope
        availableScope = ["spreadsheets.readonly", "spreadsheets", "drive.readonly", "drive"]
        if getScope in availableScope:
            self.__SCOPES = 'https://www.googleapis.com/auth/' + getScope
        else:
            self.__AvailableCheckState['state'] = False
            self.__AvailableCheckState['info'] = 'The scope is not available.'
            return
        
        # check client file
        if os.path.exists(getClientSecretFile):
            self.__CLIENT_SECRET_FILE = getClientSecretFile
        else:
            self.__AvailableCheckState['state'] = False
            self.__AvailableCheckState['info'] = 'The client secret file does not exist.'            
            return
        
        # check app name
        if len(getAppName) > 0:
            self.__APPLICATION_NAME = getAppName
        else:
            self.__AvailableCheckState['state'] = False
            self.__AvailableCheckState['info'] = 'The application name is not available.'                
            return
            
        # check all necessary components
        self.__AvailableCheckState['state'] = True
        self.__AvailableCheckState['info'] = 'All components are available.'
    
    #
    # desc : check whether sheet id or range is available or not
    #
    def __checkSheet(self, getSheetId, getRange):
         
        if len(getSheetId) > 0 and len(getRange) > 0:
            return self.__retState(True, "Both sheet ID and range are available.", {})
        else:
            return self.__retState(False, "One of sheet ID, range is not available.", {})
    
    #
    # desc : constructor
    # inpt : 
    # |- scope : https://developers.google.com/sheets/api/guides/authorizing
    # |- client secret file : absoulted path downloaded from google api console
    # |- app name : self-defined    
    #
    def __init__(self, getScope, getClientSecretFile, getAppName):
        
        self.__SCOPES = ''
        self.__CLIENT_SECRET_FILE = ''
        self.__APPLICATION_NAME = ''
        self.__AvailableCheckState = {}
    
        # check components available
        self.__checkNecessaryComponents(getScope, getClientSecretFile, getAppName)

        
    #
    # desc : fetch data from google sheets api v4
    # inpt : 
    # |- getSheetId : https://docs.google.com/spreadsheets/d/{sheet is}/edit#gid=0
    # |- getRange : query range, e.g. A:L, A2:L100, ... etc.
    # |- retType : 
    #   |- 0: returned data as dictionary format in json, 
    #       e.g. [ {col1 : data1-col1, col2 : data1-col2}, ... ]
    #   |- 1: returned data as list format in json, 
    #       e.g. [ [col1, col2, col3, ...], [data1-col1, col2-data1], ... ]
    #   |- 99: the original response from google
    #
    def fetchData(self, getSheetId, getRange, retType=0):
        
        if not self.__AvailableCheckState['state']:
            return self.__retState("failure", self.__AvailableCheckState['info'], {})
            
        if not self.__checkSheet(getSheetId, getRange)['state']:
            return self.__retState("failure", self.__checkSheet(getSheetId, getRange)['info'], {})

        credentials = self.__get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
        service = discovery.build('sheets'\
                                  , 'v4', \
                                  http=http, discoveryServiceUrl=discoveryUrl\
                                  )
    
        spreadsheetId = getSheetId
        rangeName = getRange
        result = service.spreadsheets().values().get(\
            spreadsheetId=spreadsheetId, range=rangeName\
        ).execute()
        
        # "values" is one of the items responsing from google api
        values = result.get('values', [])
    
        if not values:
            self.__retState(\
                            "success", \
                            "Both the request and API response are current but no data found.", \
                            ""\
                            )
        else:
            
            if retType == 99:
                # the same with google response
                return self.__retState("success", "Fetching data is complete.", values)
            elif retType == 1:
                # return as a list format
                return self.__retState("success", "Fetching data is complete.", values)
            else:
                # return as a dictionary format
                # check there is no duplicated colname
                if len(values[0]) != len(set(values[0])):
                    return self.__retState("failure", "Some colnames are not unique.", {})
                                        
                retList = []
                for row in range(1, len(values), 1):
                    tmp = {}
                    for item in range(0, len(values[row]), 1):
                        tmp.setdefault(values[0][item], values[row][item])
                    retList.append(tmp)
                return self.__retState("success", "Fetching data is complete.", retList)      
       
    #
    # desc : writing data into the sheet
    # inpt :
    # |- getSheetId : https://docs.google.com/spreadsheets/d/{sheet is}/edit#gid=0
    # |- getData : input values, 
    #   e.g. [["d2-1", "d2-2", "d2-3", "d2-4","d2-5"], [ another raw values ... ]]
    # |- getValueInputOptions : the type of values 
    #   {u'INPUT_VALUE_OPTION_UNSPECIFIED' | u'RAW' | u'USER_ENTERED'}
    # |- getRange : the range for data to appned
    #   e.g. A:E
    #                
    def appendData(self, getSheetId, getData, getValueInputOptions, getRange):
        
        if not self.__AvailableCheckState['state']:
            return self.__retState("failure", self.__AvailableCheckState['info'], {})
            
        if not self.__checkSheet(getSheetId, getRange)['state']:
            return self.__retState("failure", self.__checkSheet(getSheetId, getRange)['info'], {})            

        credentials = self.__get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
        service = discovery.build('sheets'\
                                  , 'v4', \
                                  http=http, discoveryServiceUrl=discoveryUrl\
                                  )
    
        spreadsheetId = getSheetId
        values = getData
        valueInputOption = getValueInputOptions
        rangeValue = getRange
        body = { 'values': values }

        result = service.spreadsheets().values().append(\
            spreadsheetId=spreadsheetId, range=rangeValue, valueInputOption=valueInputOption, body=body\
        ).execute()
        
        if (int)(result['updates']['updatedCells']) > 0:
            return self.__retState("success", result, {})
        else:
            return self.__retState("failure", result, {})











