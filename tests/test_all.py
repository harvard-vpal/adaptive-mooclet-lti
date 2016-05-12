import urllib2
import urllib
import json

def test_change_question ():
	params = { "id": 2, "text": "What is 1+0?", "answer1": 0, "answer2": 5, "answer3": -23, "answer4": 2 }
	encodedParams = urllib.urlencode(params)
	result = json.loads(urllib2.urlopen("http://localhost:8000/adaptive_engine_app/change_question?{}".format(encodedParams)).read())
	print result

def test_add_question ():
	params = { "text": "What is 1+1?", "answer1": 0, "answer2": 5, "answer3": -23, "answer4": 2 }
	encodedParams = urllib.urlencode(params)
	result = json.loads(urllib2.urlopen("http://localhost:8000/adaptive_engine_app/add_question?{}".format(encodedParams)).read())
	print result

def test_get_question ():
	result = json.loads(urllib2.urlopen("http://localhost:8000/adaptive_engine_app/get_question?question_id=2").read())
	print result

if __name__ == "__main__":
	#test_add_question()
	test_change_question()
	#test_get_question()
