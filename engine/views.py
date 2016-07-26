from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.forms import modelformset_factory,inlineformset_factory, ModelForm
from django.http import HttpResponse
from urllib import urlencode
from .models import *
from django.contrib.contenttypes.models import ContentType
from .forms import *
from .utils import *
from qualtrics.utils import provision_qualtrics_quiz
from lti.utils import display_preview

#### RESOURCE SELECTION ####

def quiz_create_options(request):
    return render(request, 'engine/quiz_create_options.html')

def quiz_create_blank(request):
    course, created = Course.objects.get_or_create(
        context = request.session['LTI_LAUNCH']['context_id'],
        name = request.session['LTI_LAUNCH']['context_title']
    )
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
        course, created = Course.objects.get_or_create(
            context = request.session['LTI_LAUNCH']['context_id'],
            name = request.session['LTI_LAUNCH']['context_title']
        )
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
    
    # redirect to an alternate view if the quiz is complete
    # grade_data = Variable.objects.get(name='quiz_grade').get_data({'quiz':quiz,'user':request.user})
    # if grade_data:
    #     grade = grade_data.last().value
    #     if grade == 1:
    #         return redirect('quiz:complete')

    # check for external url on quiz or first question of quiz
    external_url = quiz.getExternalUrl()
    if external_url:
        extra_params = {
            # pass in django user_id as a GET parameter to survey
            'user_id':request.user.id,
            'quizsource': 'preview' if display_preview(request) else 'student',
        }
        return redirect(external_url+'&'+urlencode(extra_params))

    # otherwise use django quiz app
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
    displays a form to collect question, answers and explanations
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

        #TODO create separate create_mooclet page where policy can be chosen
        # for now, set to a default policy
        policy = Policy.objects.get(name='uniform_random')

        for answer in answers:
            if not answer.mooclet:
                mooclet = Mooclet(policy=policy)
                mooclet.save()
                answer.mooclet = mooclet
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


def collaborator_request(request):
    # potential researcher would have to authenticate in the course, then open this view in a new browser window/tab (outside lms)
    # display session data, researcher sends their user id to instructor
    # TODO optional instructor could create a passcode that might be required to access this view
    # show additional info to confirm session data is correct

    return render(request, 'engine/collaborator_request.html')


def collaborator_create(request, quiz_id):
    # TODO could add confirmation mechanism: after entering id, user info is given to confirm the user

    course = Quiz.objects.get(pk=quiz_id).course

    if request.method=='POST':
        collaborator_form = CollaboratorForm(request.POST)
        collaborator = collaborator_form.save(commit=False)
        collaborator.course = course
        collaborator.save()

    collaborators = Collaborator.objects.filter(course=course)

    context = {
            'collaborator_form':CollaboratorForm(),
            'collaborators': collaborators
        }
    return render(request, 'engine/collaborator_create.html',context)


def answer_list(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answer_set.order_by('_order')
    # mooclets = [answer.mooclet for answer in answers]
    context = {
        'question':question, 
        'answers':answers, 
        # 'mooclets':mooclets,
    }
    return render(request, 'engine/answer_list.html', context)


# TODO separate view for creating mooclets?
# def mooclet_create(request):
#     if request.method == 'GET':
#     elif request.method == 'POST':
    

def mooclet_detail(request,mooclet_id):

    mooclet = get_object_or_404(Mooclet,pk=mooclet_id)
    versions = mooclet.version_set.all()
    Version_ct = ContentType.objects.get_for_model(Version)
    variables = mooclet.policy.variables.filter(content_type=Version_ct).all()

    # page used to display variables that are version-specific
    if request.method == 'GET':

        # should recieve answer_id as GET parameter, if we are navigating from an answer context
        answer = None
        if 'answer_id' in request.GET:
            answer = get_object_or_404(Answer, id=request.GET['answer_id'])


        # explanations = [version.explanation for version in mooclet.version_set.all()]

        # create m x n array of forms, where m (rows) is the number of versions and n (cols) is the number of variables
        formgroups = []
        for version in versions:
            forms = []
            for variable in variables:
                value = Value.objects.filter(object_id=version.id, variable=variable).last()              
                # TODO set auto_id to label forms in form parameters?
                if value:
                    form = VersionValueForm(instance=value)
                else:
                    form = VersionValueForm()

                forms.append(form)
            formgroups.append(forms)

        context = {
            'value_formgroups':formgroups,
            'answer':answer,
            'variables':variables,
            'versions':versions,
        }
        return render(request, 'engine/mooclet_detail.html',context)

    elif request.method == 'POST':

        # TODO figure out which form corresponds to which value/explanation/variable
        pass


