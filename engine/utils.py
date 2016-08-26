from .models import *
from django.contrib.contenttypes.models import ContentType

def get_mooclet_context(mooclet):
    # content_type for model that the mooclet is attached to
    parent_content_type = mooclet.type.content_type
    # parent object instance
    parent_content = ContentType.get_object_for_this_type(parent_content_type, pk=parent_content_id) 

    if parent_content_type.name == 'question':
        question = parent_content
    elif parent_content_type.name == 'answer':
        answer = parent_content
        question = answer.question