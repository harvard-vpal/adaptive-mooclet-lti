from dce_lti_py import OutcomeRequest
from django.conf import settings

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
        pass

    if request:
        if 'LTI_LAUNCH' in request:
            LTI_LAUNCH = request.session['LTI_LAUNCH']
        else:
            #TODO if no LTI_LAUNCH in request, do something useful
            return None
        
    elif user and quiz:
        quiz_lti_parameters = user.quizltiparameters_set.filter(quiz=quiz)
        if quiz_lti_parameters.exists():
            LTI_LAUNCH = quiz_lti_parameters.values()[0]
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