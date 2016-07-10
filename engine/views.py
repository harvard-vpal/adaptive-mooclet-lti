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
    course, created = Course.objects.get_or_create(context=request.session['LTI_LAUNCH']['context_id'])
    if created:
        course.save()

    quiz = Quiz(
        user=request.user,
        course=course,
    )
    quiz.save()
    return redirect('lti:return_launch_url', quiz_id=quiz.id)

def quiz_create_url(request):
    if request.method == 'GET':
        quiz_url_form = QuizUrlForm()
        context = {'quiz_url_form':quiz_url_form}
        return render(request, 'engine/quiz_create_url.html',context)
    elif request.method == 'POST':
        course, created = Course.objects.get_or_create(context=request.session['LTI_LAUNCH']['context_id'])
        if created:
            course.save()
        quiz_url_form = QuizUrlForm(request.POST)
        quiz = quiz_url_form.save(commit=False)
        quiz.course = course
        quiz.user = request.user
        quiz.save()

        return redirect('lti:return_launch_url', quiz_id=quiz.id)


#### UTILITY VIEWS ####

def quiz_display(request, quiz_id):
    '''
    Redirect to proper mode of displaying quiz, based on urls present in quiz model fields
    '''
    quiz = get_object_or_404(Quiz,pk=quiz_id)
    external_url = quiz.getExternalUrl()

    # redirect to an alternate view if the quiz is complete
    if Outcome.objects.filter(user=request.user, quiz=quiz).exists():
        outcome = Outcome.objects.get(user=request.user, quiz=quiz)
        if outcome.grade==1:
            return redirect('quiz:complete')

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

def launch_sandbox(request):
    '''
    non-lti launch that redirects user to a shared default sandbox quiz (instructor view)
    '''
    quiz = Quiz.objects.get(pk=1)
    request.session['quiz_id'] = quiz.pk
    return redirect('engine:quiz_detail', quiz_id=quiz_id)

def launch_sandbox_quiz(request):
    '''
    convenience view/url for launching sandbox quiz (student view)
    '''
    return redirect('engine:quiz_display', quiz_id=1)


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

    # get existing or initialize question object
    if quiz.question_set.all().exists():
        question = quiz.question_set.first()
    else:
        question = Question(quiz=quiz)

    # handle form display
    if request.method == 'GET':

        INITIAL_NUM_CHOICES = 4
        INITIAL_NUM_EXPLANATIONS = 2
        
        AnswerFormset = inlineformset_factory(Question, Answer, form=AnswerForm, fields=('text','correct'), can_delete=False, extra=4, max_num=4)
        
        # set initial value for use_qualtrics checkbox
        use_qualtrics = True
        if quiz.question_set.all().exists():
            use_qualtrics = bool(quiz.question_set.first().url)

        quiz_form = QuizForm(instance=quiz,initial={'use_qualtrics':use_qualtrics})

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
        answers = answer_formset.save(commit=False)
        # associate mooclet instances with each answer before saving
        for answer in answers:
            if not answer.mooclet:
                mooclet = Mooclet()
                mooclet.save()
                answer.mooclet = Mooclet()
            answer.save()

        quiz_form.is_valid()
        if quiz_form.cleaned_data['use_qualtrics'] and not question.url:
            
            print "starting quiz provisioning process"

            new_survey_url = provision_qualtrics_quiz(request, question)
            
            if not new_survey_url:
                raise Exception('quiz creation failed and did not return a qualtrics id')

            question.url = new_survey_url

        # remove url field if checkbox deselected
        if not quiz_form.cleaned_data['use_qualtrics'] and question.url:
            question.url = ''

            # TODO: delete the corresponding survey on qualtrics
            # delete_qualtrics_quiz(request, survey_url)

        question.save()

        return redirect('engine:quiz_detail', quiz_id=quiz_id)


def explanation_list(request, quiz_id):
    '''
    list explanations for a single question (multiple choices)
    '''
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question = quiz.question_set.first()
    answers = question.answer_set.order_by('_order')
    context = {'answers':answers, 'quiz':quiz}

    return render(request, 'engine/explanation_list.html', context)


def explanation_create(request, mooclet_id):
    '''
    create new explanation version
    '''
    mooclet = get_object_or_404(Mooclet,pk=mooclet_id)

    if request.method=='GET':
        context = {
            'explanation_form':ExplanationForm()
        }
        return render(request, 'engine/explanation_create.html',context)

    elif request.method=='POST':
        explanation_form = ExplanationForm(request.POST)
        explanation = explanation_form.save(commit=False)
        explanation.mooclet = mooclet
        explanation.save()

        return redirect('engine:explanation_list',quiz_id=request.session['quiz_id'])


def explanation_modify(request, explanation_id):
    '''
    modify an explanation version
    '''
    explanation = get_object_or_404(Explanation,pk=explanation_id)
    mooclet = explanation.mooclet

    if request.method=='GET':
        context = {
            'explanation_form':ExplanationModifyForm(instance=explanation)
        }
        return render(request, 'engine/explanation_modify.html',context)

    elif request.method=='POST':
        explanation_form = ExplanationModifyForm(request.POST,instance=explanation)
        explanation_form.is_valid()
        if explanation_form.cleaned_data['delete']:
            explanation = explanation.delete()
        else:
            explanation = explanation_form.save()


        
        return redirect('engine:explanation_list',quiz_id=request.session['quiz_id'])


# def ExplanationCreate(generic.edit.CreateView):
#     model = Explanation
#     fields = ['text']


def collaborator_request(request):
    # potential researcher would have to authenticate in the course, then open this view in a new browser window/tab (outside lms)
    # display session data, researcher sends their user id to instructor
    # TODO optional instructor could create a passcode that might be required to access this view
    # show additional info to confirm session data is correct

    return render(request, 'engine/collaborator_request.html')

# class ResearcherCreate(generic.edit.CreateView):

#     # add researcher to a course
#     model = Researcher
#     fields = ['user','user_lms_id']

#     def form_valid(self,form):
#         researcher = form.save(commit=False)
#         researcher.course = Course.objects.get(context=self.request['LTI_LAUNCH']['context_id'])
#         return super(ResearcherCreate, self).form_valid(form)


def collaborator_create(request, quiz_id):
    # TODO could add confirmation mechanism: after entering id, user info is given to confirm the user
    if request.method=='GET':
        pass

    if request.method=='POST':
        collaborator_form = CollaboratorForm(request.POST)
        collaborator = collaborator_form.save()

    collaborators = Collaborator.objects.all()
    # filter by course?
    # filter by mooclet?

    context = {
            'collaborator_form':CollaboratorForm(),
            'collaborators': collaborators
        }
    return render(request, 'engine/collaborator_create.html',context)



def answer_list(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answer_set.order_by('_order')
    context = {'question':question, 'answers':answers}
    return render(request, 'engine/answer_list.html', context)


def answer_detail(request,answer_id):

    if request.method == 'GET':
        answer = get_object_or_404(Answer,pk=answer_id)
        explanations = answer.explanation_set

        mooclet_version_variable_ids = [1,2]

        explanation_ids = [1,2,3]

        # https://docs.djangoproject.com/en/1.9/topics/forms/modelforms/#model-formsets
        # changing the queryset
        # MoocletVersionVariableValueFormset = formset_factory(MoocletVersionVariableValue, fields=('value',), can_delete=False, extra=4, max_num=4)
        # mooclet_version_variable_value_formset = MoocletVersionVariableValueFormset()



        mooclet_version_variable_value_forms = []

        for mooclet_version_variable_id in mooclet_version_variable_ids:

            forms_for_variable_type = []

            for explanation in explanations.all():

                mooclet_version_variable = MoocletVersionVariable.objects.get(pk=mooclet_version_variable_id)
                
                # get or create variable_value_for_explanation
                variable_value_for_explanation_qset = MoocletVersionVariableValue.objects.filter(
                    mooclet_version_variable = mooclet_version_variable,
                    explanation = explanation
                )
                if variable_value_for_explanation_qset.exists():
                    variable_value_for_explanation = variable_value_for_explanation_qset.first()
                else: # create
                    variable_value_for_explanation = MoocletVersionVariableValue(
                        mooclet_version_variable = mooclet_version_variable,
                        explanation = explanation,
                        # value = ?
                    )

                # TODO some kind of form labelling
                mooclet_version_variable_value_form = MoocletVersionVariableValueForm(instance=variable_value_for_explanation)
                forms_for_variable_type.append(mooclet_version_variable_value_form)

            mooclet_version_variable_value_forms.append(forms_for_variable_type)



        # vars = [MoocletVersionVariable1, MoocletVersionVariable2]
        # for MoocletVersionVariable in vars:
            # generate a form for each moocletversion
            # formset = [form1, form2, form3, form4]

        context = {
            'answer':answer,
            'mooclet_version_variable_value_forms': mooclet_version_variable_value_forms
        }

        return render(request, 'engine/answer_detail.html',context)

    elif request.method == 'POST':

        # how do we figure out which form corresponds to which value/explanation/variable

        pass

# # MoocletVersionVariableValueForm
#         AnswerFormset = formset_factory(Question, Answer, form=AnswerForm, fields=('text','correct'), can_delete=False, extra=4, max_num=4)
#         answer_formset = AnswerFormset(instance=question)



