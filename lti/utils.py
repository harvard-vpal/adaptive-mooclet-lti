from dce_lti_py import OutcomeRequest
from django.conf import settings
from  engine.models import Quiz


def display_preview(request):
    '''
    Checks whether to launch the LTI tool in preview mode or quiz mode
    Returns True for preview, False for quiz
    '''
    quiz = Quiz.objects.get(id=request.session['quiz_id'])
    # LTI User role check
    user_roles = request.session['LTI_LAUNCH']['roles']
    if 'Instructor' in user_roles or 'ContentDeveloper' in user_roles:
        return True

    # collaborator check
    if request.user.collaborator_set.filter(course=quiz.course).exists():
        return True

    return False


def grade_passback(grade=None, request=None, user=None, quiz=None):
    '''
    Return grade / outcome data back to the LMS via LTI Outcome Service protocol
    To get grade passback url, either provide: 
        request (used to get LTI params) 
    or
        user/quiz combo (used to retrieve LTI params stored in db)
    
    '''
    if not grade:
        # TODO get grade from value store, would require user/quiz in parameters
        return None

    if request:
        if 'LTI_LAUNCH' in request:
            LTI_LAUNCH = request.session['LTI_LAUNCH']
        else:
            #TODO if no LTI_LAUNCH in request, do something useful
            return None
        
    elif user and quiz:
        lti_parameters = user.ltiparameters_set.filter(quiz=quiz)
        if lti_parameters.exists():
            LTI_LAUNCH = lti_parameters.values()[0]
    else:
        pass

    # send the outcome data
    outcome = OutcomeRequest(
        {
            # required for outcome reporting
            'lis_outcome_service_url':LTI_LAUNCH['lis_outcome_service_url'],
            'lis_result_sourcedid':LTI_LAUNCH['lis_result_sourcedid'],
            'consumer_key': LTI_LAUNCH['oauth_consumer_key'],
            'consumer_secret': settings.LTI_OAUTH_CREDENTIALS[LTI_LAUNCH['oauth_consumer_key']],
            'message_identifier': 'myMessage'
        }
    )
    
    outcome_response = outcome.post_replace_result(
        grade,
        # result_data={
        # #     # 'url':'placeholder'
        #     'text':'complete'
        # }
    )
    print 'GRADE PASSBACK'
    print grade, LTI_LAUNCH
    print outcome_response

    # TODO error detection on bad passback
    return outcome_response