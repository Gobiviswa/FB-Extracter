#!/usr/bin/env python
import sys           #to getversion of Python 
import json          #for handling JSON files
import requests      #for requesting URL content        
import getpass       #for getting password
import time
import datetime
import csv

#getting the version of the python 
def getVersion():
        if sys.version_info[0] > 2:
                return input
        else:
                return raw_input

#inputting the page id of the particular page
def pageId():
        page_id = inputType("Please enter the page id --> ")
        return str(page_id)


#inputting the credentials of our fb developer app
def appCred():
        app_id = inputType("Please enter the App id --> ")
        app_secret = getpass.getpass("Please enter the App Secret Id --> ")
        return app_id , app_secret

#creating token automatically fron app credentials given above
def getFbToken(app_id, app_secret):
        payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
        file = requests.post('https://graph.facebook.com/oauth/access_token?', params = payload)
        #print file.text #to test what the FB api responded with    
        token = file.text.split("=")
        access = json.loads(token[0])
        access_token = access["access_token"]
        return str(access_token)

def validateDate(date):
        try:
                datetime.datetime.strptime(date, "%d/%m/%Y")
        except :
                raise ValueError("Please give in dd/mm/yyyy format")

#dates for the duration
def getDates():
        since = inputType("Please enter the start date in DD/MM/YYYY format --> ")
        validateDate(since)
        until = inputType("Please enter the end date in DD/MM/YYYY format --> ")
        validateDate(until)
        since_unix = time.mktime(datetime.datetime.strptime(since , "%d/%m/%Y").timetuple())
        until_unix = time.mktime(datetime.datetime.strptime(until , "%d/%m/%Y").timetuple())
        return str(since.replace('/','-')), str(until.replace('/','-')), str(since_unix) , str(until_unix)

def getTime():
        time = datetime.datetime.now().time()

        return str(time.hour) + "-" + str(time.minute) + "-" + str(time.second)


#processing the url we have created
def processURL(url):
        while True:
                dic = requests.get(url).json()
                file_name = "data_" + start_date + "_" + end_date + "_" + time + ".csv"
                csvObj = open(file_name , 'a')
                csv_file = csv.writer(csvObj)
                if dic["data"] != {}:
                        for element in dic["data"]:
                                post_id , post_time = element["id"] , element["created_time"][0:10]
                                if "message" not in element:
                                        element["message"] = ""
                                post_message = element["message"].encode('utf-8')
                                if "comments" not in element:
                                        element["comments"] = {}
                                        element["comments"]["summary"] = {}
                                        element["comments"]["summary"]["total_count"] = 0
                                post_comments_count = element["comments"]["summary"]["total_count"]
                                if "likes" not in element:
                                        element["likes"] = {}
                                        element["likes"]["summary"] = {}
                                        element["likes"]["summary"]["total_count"] = 0
                                post_likes_count = element["likes"]["summary"]["total_count"]
                                if "shares" not in element:
                                        element["shares"] = {}
                                        element["shares"]["count"] = 0
                                post_shares_count = element["shares"]["count"]
                                csv_file . writerow([post_id , post_time , post_message  , post_comments_count , post_likes_count , post_shares_count ])
#                               
                else:
                        break

                if "paging" in dic:
                        url = dic["paging"]["next"]
                else:
                        break

                        
inputType = getVersion()
page_id = pageId()
app_id , app_secret = appCred()
token = getFbToken(app_id, app_secret)
start_date, end_date, s_date , u_date = getDates()
time = getTime()
#forming the url
url = "https://graph.facebook.com/"+page_id+"/posts?fields=id,message,created_time,likes.limit(0).summary(true),comments.limit(0).summary(true),shares&since="+s_date+"&until="+u_date+"&access_token="+token
processURL(url)
