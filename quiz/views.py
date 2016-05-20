from django.shortcuts import render

# Create your views here.
def display_quiz_question(request, quiz_id):
    '''
    self-hosted quiz: display initial question and prompt for answer choice
    '''
    # using communication protocol to make semantic decision?
    if not request.method=='POST':
        quiz = Quiz.objects.get(pk=quiz_id)
        # just get first question in quiz for now
        question = quiz.question_set.first()
        answers = question.answer_set.all().order_by('order')

        # could simulate web service request to get: questions, answers
        # question_data = requests.get(reverse('adaptive_engine:get_question'),params={'id':question.id})
        # question_text = question_data['text']

        # alternative: get objects directly
        choose_answer_form = ChooseAnswerForm()
        choose_answer_form.fields['answer'].queryset = answers

        context = {
            'question':question,
            'choose_answer_form': choose_answer_form,
        }

        return render(request, 'qlb/display_quiz_question.html', context)

    else:
        choose_answer_form = ChooseAnswerForm(request.POST)
        if choose_answer_form.is_valid():
            answer = choose_answer_form.cleaned_data['answer']

            # get explanation
            # make API call to adaptive engine
            # url = 'https://'+request.get_host()+reverse('adaptive_engine:get_explanation_for_student')
            # explanation_id = requests.get(
            #     url,
            #     params={
            #         'student_id':request.user.id,
            #         'answer_id':answer.id
            #     }
            # ).json()['explanation']

            # placeholder student id
            student_id = 'placeholder'

            # alternative: call function directly
            allExplanations = []
            allResultsForExplanations = []
            for explanation in Explanation.objects.filter(answer=answer).iterator():
                someResults = []
                for result in Result.objects.filter(explanation=explanation).iterator():
                    someResults.append(result.value)
                allResultsForExplanations.append(someResults)
                allExplanations.append(explanation)
            selectedExplanation, exp_value = computeExplanation_Thompson(student_id, allExplanations, allResultsForExplanations)

            

            # explanation = Explanation.get(pk=explanation_id)

            # redirect to explanation view
            return HttpResponseRedirect(reverse('qlb:display_quiz_explanation',kwargs={'explanation_id':selectedExplanation.id}))

def display_quiz_explanation(request, explanation_id):
    '''
    self-hosted quiz: show explanation and let student rate the explanation
    '''
    explanation = Explanation.objects.get(pk=explanation_id)

    if not request.method=='POST':
        rate_explanation_form = RateExplanationForm()

        context = {
            'explanation':explanation,
            'rate_explanation_form':rate_explanation_form
        }

        return render(request, 'qlb/display_quiz_explanation.html', context)

    else:
        print "posted to display_quiz_explanation"
        # process student rating for explanation
        rate_explanation_form = RateExplanationForm(request.POST)
        if rate_explanation_form.is_valid():
            rating = rate_explanation_form.cleaned_data['rating']

            # save to db
            rating = Result(student=request.user, explanation=explanation, value=rating)
        return HttpResponseRedirect(reverse('qlb:end_of_quiz'))
