from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.forms import formset_factory,inlineformset_factory, ModelForm
from django.http import HttpResponse
from urllib import urlencode

from .models import *
from .forms import *
from .utils import *
from .algorithms import computeExplanation_Thompson

from qualtrics.utils import provision_qualtrics_quiz

from django.views import generic

#### RESOURCE SELECTION ####

def quiz_create_options(request):
    return render(request, 'engine/quiz_create_options.html')

def quiz_create_blank(request):
    quiz = Quiz(
        user=request.user,
        context = request.session['LTI_LAUNCH']['context_id'],
    )
    quiz.save()
    return redirect('lti:return_launch_url', quiz_id=quiz.id)

def quiz_create_url(request):
    if request.method == 'GET':
        quiz_url_form = QuizUrlForm()
    pass


#### REDIRECTION UTILITY VIEW ####

def quiz_display(request, quiz_id):
    '''
    Redirect to proper mode of displaying quiz, based on urls present in quiz model fields
    '''
    quiz = get_object_or_404(Quiz,pk=quiz_id)
    external_url = quiz.getExternalUrl()

    if external_url:
        extra_params = {
            'user_id':request.user.id,
        }
        return redirect(external_url+'&'+urlencode(extra_params))
    else:
        if quiz.question_set.all().exists():
            question = quiz.question_set.first()
            return redirect('quiz:question',question_id=question.id)
        else:
            return redirect('quiz:placeholder')


#### QUIZ MANAGEMENT ####

def quiz_detail(request, quiz_id):
    '''
    Quiz management home for instructors
    '''
    quiz = Quiz.objects.get(pk=quiz_id)
    context = {'quiz':quiz}

    return render(request, 'engine/quiz_detail.html', context)

# def manage_quiz(request, quiz_id):
#     '''
#     Teacher view for a quiz
#     '''
#     quiz = Quiz.objects.get(pk=quiz_id)
#     context = {
#         'quiz': quiz,
#     }
#     return render(request, 'engine/manage_quiz.html',context)


def quiz_update(request, quiz_id):
    '''
    displays some a form to collect question, answers and explanations
    '''
    quiz = Quiz.objects.get(pk=quiz_id)

    # determine whether question is being created or modified
    if quiz.question_set.all().exists():
        question = quiz.question_set.first()
    else:
        question = Question(quiz=quiz)

    # set initial value for use_qualtrics checkbox
    use_qualtrics = True
    if quiz.question_set.all().exists():
        use_qualtrics = bool(quiz.question_set.first().url)
    
    # handle form display
    if request.method == 'GET':

        INITIAL_NUM_CHOICES = 4
        INITIAL_NUM_EXPLANATIONS = 2
        
        AnswerFormset = inlineformset_factory(Question, Answer, form=AnswerForm, fields=('text','correct'), can_delete=False, extra=4, max_num=4)
        
        quiz_form = QuizForm(instance=quiz,initial={'use_qualtrics':False})

        question_form = QuestionForm(instance=question)

        answer_formset = AnswerFormset(instance=question)

        context = {
            # 'quiz_form':CreateQuizForm(),
            # 'Question':ModelForm(Question),
            'quiz':quiz,
            'quiz_form':quiz_form,
            'question_form':question_form,
            'answer_formset': answer_formset,
            # 'answer_formgroups':answer_formgroups,
        }

        return render(request, 'engine/quiz_update.html', context)

    # handle form submission/processing
    elif request.method == 'POST':

        quiz_form = QuizForm(request.POST, instance=quiz)
        quiz = quiz_form.save(commit=False)

        # quiz.course = 7566
        if 'LTI_LAUNCH' in request.session:
            quiz.context = request.session['LTI_LAUNCH']['context_id']
        quiz.user = request.user
        quiz.save()

        question_form = QuestionForm(request.POST, instance=question)
        question = question_form.save(commit=False)
        question.save()

        AnswerFormset = inlineformset_factory(Question, Answer, fields=('text','correct'), can_delete=False, extra=4, max_num=4)
        answer_formset = AnswerFormset(request.POST, instance=question)
        answers = answer_formset.save()

        quiz_form.is_valid()
        if quiz_form.cleaned_data['use_qualtrics'] and not question.url:

            
            print "starting quiz provisioning process"

            new_survey_url = provision_qualtrics_quiz(request, question)
            
            if not new_survey_url:
                raise Exception('quiz creation failed and did not return a qualtrics id')

            question.url = new_survey_url
            question.save()


        # TODO remove url field if checkbox deselected
        # elif quiz_form.clear


        return redirect('engine:quiz_detail', quiz_id=quiz_id)


def explanation_list(request, quiz_id):
    '''
    list explanations for a single question (multiple choices)
    '''
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question = quiz.question_set.first()
    answers = question.answer_set.order_by('order')
    context = {'answers':answers, 'quiz':quiz}

    return render(request, 'engine/explanation_list.html', context)



def explanation_create(request, answer_id):
    answer = get_object_or_404(Answer,pk=answer_id)

    if request.method=='GET':
        context = {
            'answer':answer,
            'explanation_form':ExplanationForm()
        }
        return render(request, 'engine/explanation_create.html',context)

    elif request.method=='POST':
        explanation_form = ExplanationForm(request.POST)
        explanation = explanation_form.save(commit=False)
        explanation.answer = answer
        explanation.save()

        return redirect('engine:explanation_list',quiz_id=answer.question.quiz.id)

def explanation_modify(request, explanation_id):
    explanation = get_object_or_404(Explanation,pk=explanation_id)
    answer = explanation.answer

    if request.method=='GET':
        context = {
            'explanation_form':ExplanationForm(instance=explanation)
        }
        return render(request, 'engine/explanation_modify.html',context)

    elif request.method=='POST':
        explanation_form = ExplanationForm(request.POST,instance=explanation)
        explanation = explanation_form.save()
        
        return redirect('engine:explanation_list',quiz_id=request.session['quiz_id'])


# def ExplanationCreate(generic.edit.CreateView):
#     model = Explanation
#     fields = ['text']


def researcher_request(request):
    # potential researcher would have to authenticate in the course, then open this view in a new browser window/tab (outside lms)
    # display session data, researcher sends their user id to instructor
    # TODO optional instructor could create a passcode that might be required to access this view
    # show additional info to confirm session data is correct

    return render(request, 'engine/researcher_request.html')

# class ResearcherCreate(generic.edit.CreateView):

#     # add researcher to a course
#     model = Researcher
#     fields = ['user','user_lms_id']

#     def form_valid(self,form):
#         researcher = form.save(commit=False)
#         researcher.course = Course.objects.get(context=self.request['LTI_LAUNCH']['context_id'])
#         return super(ResearcherCreate, self).form_valid(form)


def researcher_create(request):
    # TODO could add confirmation mechanism: after entering id, user info is given to confirm the user
    if request.method=='GET':
        context = {
            'researcher_form':ResearcherForm(),
        }
        return render(request, 'engine/researcher_create.html',context)
    if request.method=='POST':
        researcher_form = ResearcherForm(request.POST)







