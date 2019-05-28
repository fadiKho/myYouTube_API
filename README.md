Python YouTube RESTful API

A basic Python YouTube Data API to fetch data from YouTube using public API-Key without OAuth
It fetches videos, and performs search and return videos.
You are required to get the API key from Google API console in order to use this script.

System requirements
- Python
- Python libraries:
	- flask 
	- json
	- requests

How to use
1- deploy the app in your localhost, using the commands:
	set FLASK_APP=myYouTubeApi.py
	python -m flask run
2- now you can fetch data by passing URLs from your browser - replace each <parameter> with your relevant value:
	- videos by YouTube VideoId:
		URL: http://localhost:5000/videos?id=<VIDEOID>&key=<YOR_YOUTUBE_API_KEY>
		<VIDEOID> - YouTube video ID
		<YOR_YOUTUBE_API_KEY> - your personal YouTube API key you got from YouTube API Console
	- search videos by search terms:
		URL: http://localhost:5000/search?term=<SEARCH_TERM>&count=<NUM_OF_RESULTS>&key=<YOR_YOUTUBE_API_KEY>
		<SEARCH_TERM> - the search term
		<NUM_OF_RESULTS> - the maximun number of results wanted
		<YOR_YOUTUBE_API_KEY> - your personal YouTube API key you got from YouTube API Console
	- get your recent search terms:
		URL: http://localhost:5000/getRecent?count=<NUM_OF_RESULTS>
		<NUM_OF_RESULTS> - the maximun number of results wanted
