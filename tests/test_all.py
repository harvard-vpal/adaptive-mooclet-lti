import urllib2
import urllib
import json

def test_submit_result_of_explanation ():
	params = { "explanation_id": 1, "student_id": 1, "value": 3 }
	encodedParams = urllib.urlencode(params)
	result = json.loads(urllib2.urlopen("http://localhost:8000/adaptive_engine_app/submit_result_of_explanation?{}".format(encodedParams)).read())
	print result

def test_get_explanation_for_student ():
	params = { "question_id": 2, "student_id": 1 }
	encodedParams = urllib.urlencode(params)
	result = json.loads(urllib2.urlopen("http://localhost:8000/adaptive_engine_app/get_explanation_for_student?{}".format(encodedParams)).read())
	print result

def test_add_explanation ():
	params = { "text": "If you combine one marble and another marble, you get two marbles.", "question_id": 2, "answer_id": 4 }
	encodedParams = urllib.urlencode(params)
	result = json.loads(urllib2.urlopen("http://localhost:8000/adaptive_engine_app/add_explanation?{}".format(encodedParams)).read())
	print result

def test_change_explanation ():
	params = { "text": "If you combine one marble and another marble, you get two marbles.", "id": 1, "question_id": 2, "answer_id": 4 }
	encodedParams = urllib.urlencode(params)
	result = json.loads(urllib2.urlopen("http://localhost:8000/adaptive_engine_app/change_explanation?{}".format(encodedParams)).read())
	print result

def test_get_explanations_for_question ():
	result = json.loads(urllib2.urlopen("http://localhost:8000/adaptive_engine_app/get_explanations_for_question?question_id=2").read())
	print result

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
	test_add_question()
	test_change_question()
	test_get_question()
	test_get_explanations_for_question()
	test_add_explanation()
	test_change_explanation()
	test_get_explanation_for_student()
	test_submit_result_of_explanation()
