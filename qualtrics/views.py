from django.shortcuts import render

# Create your views here.

def create_qualtrics_quiz_from_url(request):
    if request.method == 'GET':
        context = {
            'qualtrics_quiz_form':QualtricsUrlQuizForm(),
        }
        return render(request, 'lti/create_qualtrics_quiz_from_url.html', context) 
    else:
        qualtrics_quiz_form = QualtricsUrlQuizForm(request.POST)
        quiz = qualtrics_quiz_form.save(commit=False)
        # placeholder
        quiz.course = 7566 
        quiz.user = request.user
        quiz.save()

        # alternatively, could redirect back to select_or_create_quiz and have user select the quiz they just created
        return HttpResponseRedirect(reverse('lti:embed_quiz',kwargs={'quiz_id':quiz.pk}))

def qsf_for_quiz(request, quiz_id):
    '''
    view that generates the qsf corresponding to the quiz_id provided as input
    '''
    quiz = Quiz.objects.get(pk=quiz_id)
    quiz_qsf = modify_qsf_template(quiz)
    return HttpResponse(quiz_qsf)
