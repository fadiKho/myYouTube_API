"""
========================
Python YouTube API
========================
Developed by: Fadi Khoury
Email: fady.kho@gmail.com
========================
This program is a RESTful API which is an interface for YouTube Data API service
that can fetch specific sorts of user data by user requests.
For more information - please read the README document attached to the project.
========================
"""

from flask import Flask, request, Response, make_response
from flask_restful import Resource, Api
import requests
import json

app = Flask(__name__)
api = Api(app)

MAX_RESULTS = 100

class Search(Resource):
	def get(self):
	
		term  = request.args.get('term')
		count = request.args.get('count')
		key  = request.args.get('key')
		
		PARAMS = {  'part':"snippet",
					'maxResults':count,
					'q':term,
					'type':"video",				
					'key': key} 
					
		resp = requests.get('https://www.googleapis.com/youtube/v3/search', params=PARAMS)
		searchResults = {}
		searchResults['videos'] = []
		
		for i in range(int(count)):
			jsResp = resp.json()
			vid = jsResp["items"][i]["id"]["videoId"]
			v = Videos()
			vRes = v.get(vid,key)
			jsV = json.loads(vRes)
			searchResults['videos'].append(jsV)
			
		res = make_response(json.dumps(searchResults))
		dq = addTermToJson(term)
		res.set_cookie('recentlySearched', dq)
		
		return (res) 	

class Videos(Resource):
	def get(self, id='', key=''):
	
		if (id == ''):
			id  = request.args.get('id')
			key  = request.args.get('key')
			
		PARAMS = {  'part':"snippet,contentDetails",
					'id':id,
					'key': key} 
					
		resp = requests.get('https://www.googleapis.com/youtube/v3/videos', params=PARAMS)
		jsResp = resp.json()
		parsed = getTitleDurationFromVid(jsResp)
		
		return (json.dumps(parsed)) 
	
@app.route("/getRecent")	
def getLast (count=''):

	count = int(request.args.get('count'))
	
	if (request.cookies.get('recentlySearched')):
		dq = request.cookies.get('recentlySearched')
	else:
		return "No recent searches!"
	
	bC = bytearray(dq, 'utf-8')
	jsn = bC.decode('utf8').replace("'", '"')
	jason = json.loads(jsn)
	
	if (count > len(jason['search_terms'])):
		count = len(jason['search_terms'])
		
	jason['search_terms'] = jason['search_terms'][len(jason['search_terms']) - count:]
		
	return json.dumps(jason)
	
def addTermToJson(term):

	if (request.cookies.get('recentlySearched')):
		strC = request.cookies.get('recentlySearched')
		bC = bytearray(strC, 'utf-8')
		jsn = bC.decode('utf8').replace("'", '"')
		jason = json.loads(jsn)
		
		if (len(jason['search_terms']) < MAX_RESULTS):
			jason['search_terms'].append(term)
		else:
			del jason['search_terms'][0]
			jason['search_terms'].append(term)
			
	else:
		jason = {}
		jason['search_terms'] = []
		jason['search_terms'].append(term)
		
	bjsn = json.JSONEncoder().encode(jason)
	
	return bjsn

def getTitleDurationFromVid (js):
	data = {}
	data["title"] = js["items"][0]["snippet"]["title"]
	strDur = js["items"][0]["contentDetails"]["duration"]

	if (strDur[0:2] == "PT"): 
		strDur = strDur[2:]
		dur = ""
		j = 0
		i = strDur.find("D", 0)
		if (i > -1): 
			dur = strDur[j : i] + ":"
			j = i + 1
		i = strDur.find("H", 0)
		if (i > -1): 
			dur = dur + strDur[j : i] + ":"
			j = i + 1
		i = strDur.find("M", 0)
		if (i > -1): 
			dur = dur + strDur[j : i] + ":"
			j = i + 1
		i = strDur.find("S", 0)
		if (i > -1): 
			dur = dur + strDur[j : i]
			j = i + 1
		data['duration'] = dur
	else:
		data['duration'] = strDur
		
	return data

def getVideoIdFromSearchRes (js, i):
	return js["items"][i]["id"]["videoId"]

api.add_resource(Videos, '/videos') # Route_1
api.add_resource(Search, '/search') # Route_2


if __name__ == '__main__':
	app.run(debug = True)
	