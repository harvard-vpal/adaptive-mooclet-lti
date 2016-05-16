import urllib2
import urllib
import json

#URL = "http://localhost:8000"
URL = "http://adaptive-engine-dev.us-east-1.elasticbeanstalk.com"

def test_submit_result_of_explanation (explanation_id):
	params = { "explanation_id": explanation_id, "student_id": 1, "value": 3 }
	encodedParams = urllib.urlencode(params)
	result = json.loads(urllib2.urlopen(URL + "/adaptive_engine_app/submit_result_of_explanation?{}".format(encodedParams)).read())
	print result

def test_get_explanation_for_student (question_id):
	params = { "question_id": question_id, "student_id": 1, "answer_id": 4 }
	encodedParams = urllib.urlencode(params)
	result = json.loads(urllib2.urlopen(URL + "/adaptive_engine_app/get_explanation_for_student?{}".format(encodedParams)).read())
	print result

def test_add_explanation (question_id):
	params = { "text": "If you combine one marble and another marble, you get two marbles.", "question_id": question_id, "answer_id": 4 }
	encodedParams = urllib.urlencode(params)
	result = json.loads(urllib2.urlopen(URL + "/adaptive_engine_app/add_explanation?{}".format(encodedParams)).read())
	print result
	return result['id']

def test_change_explanation (question_id, explanation_id):
	params = { "text": "If you combine one marble and another marble, you get two marbles.", "id": explanation_id, "question_id": question_id, "answer_id": 4 }
	encodedParams = urllib.urlencode(params)
	result = json.loads(urllib2.urlopen(URL + "/adaptive_engine_app/change_explanation?{}".format(encodedParams)).read())
	print result

def test_get_explanations_for_question (question_id):
	result = json.loads(urllib2.urlopen(URL + "/adaptive_engine_app/get_explanations_for_question?question_id={}".format(question_id)).read())
	print result

def test_change_question (question_id):
	params = { "id": question_id, "text": "What is 1+0?", "answer1": 0, "answer2": 5, "answer3": -23, "answer4": 2 }
	encodedParams = urllib.urlencode(params)
	result = json.loads(urllib2.urlopen(URL + "/adaptive_engine_app/change_question?{}".format(encodedParams)).read())
	print result

def test_add_question ():
	params = { "text": "What is 1+1?", "answer1": 0, "answer2": 5, "answer3": -23, "answer4": 2 }
	encodedParams = urllib.urlencode(params)
	result = json.loads(urllib2.urlopen(URL + "/adaptive_engine_app/add_question?{}".format(encodedParams)).read())
	print result
	return result['id']

def test_get_question (question_id):
	result = json.loads(urllib2.urlopen(URL + "/adaptive_engine_app/get_question?id={}".format(question_id)).read())
	print result

def test_remove_question (question_id):
	result = json.loads(urllib2.urlopen(URL + "/adaptive_engine_app/remove_question?id={}".format(question_id)).read())
	print result

if __name__ == "__main__":
	question_id = test_add_question()
	test_change_question(question_id)
	test_get_question(question_id)
	explanation_id = test_add_explanation(question_id)
	test_get_explanations_for_question(question_id)
	test_change_explanation(question_id, explanation_id)
	test_get_explanation_for_student(question_id)
	test_submit_result_of_explanation(explanation_id)
	test_remove_question(question_id)
