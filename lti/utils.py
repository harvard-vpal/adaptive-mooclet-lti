from dce_lti_py import OutcomeRequest
from django.conf import settings
from quip.models import Quiz
from lti.models import LtiParameters


def display_preview(user, quiz):
    '''
    Checks whether to launch the LTI tool in preview mode or quiz mode for a given user and quiz
    Returns True for preview, False for quiz
    '''
    lti_parameters = LtiParameters.objects.get(user=user, quiz=quiz)

    # LTI User role check
    user_roles = lti_parameters.roles
    if 'Instructor' in user_roles or 'ContentDeveloper' in user_roles or 'TeachingAssistant' in user_roles:
        return True

    # collaborator check
    if user.collaborator_set.filter(course=quiz.course).exists():
        return True

    return False


def grade_passback(grade, user, quiz):
    '''
    Return grade / outcome data back to the LMS via LTI Outcome Service protocol
    To get grade passback url, either provide: 
        request (used to get LTI params) 
    or
        user/quiz combo (used to retrieve LTI params stored in db)
    
    '''
    lti_parameters = LtiParameters.objects.get(user=user, quiz=quiz)

    # send the outcome data
    outcome = OutcomeRequest(
        {
            # required for outcome reporting
            'lis_outcome_service_url':lti_parameters.lis_outcome_service_url,
            'lis_result_sourcedid':lti_parameters.lis_result_sourcedid,
            'consumer_key': lti_parameters.oauth_consumer_key,
            'consumer_secret': settings.LTI_OAUTH_CREDENTIALS[lti_parameters.oauth_consumer_key],
            'message_identifier': 'myMessage'
        }
    )
    
    outcome_response = outcome.post_replace_result(grade)

    # error logging
    print 'GRADE PASSBACK TRIGGERED: user={}, quiz={}, course={}, grade={}'.format(user.pk, quiz.pk, course.pk, grade)
    print outcome_response

    # TODO error detection on bad passback
    return outcome_response
