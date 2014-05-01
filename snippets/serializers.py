from django.contrib.auth.models import User
from django.forms import widgets
from rest_framework import serializers
from rest_framework.exceptions import APIException

from snippets.models import Snippet, SnippetExtra, LANGUAGE_CHOICES, STYLE_CHOICES

class ImproperExpandException(APIException):
    status_code = 500
    default_detail = 'The expansion mapping was not configured properly'

def split_expands(obj):
    if not isinstance(obj.expand, list):
        obj.expand = [a.strip() for a in obj.expand.split(',') if a.strip()]
    for e in obj.expand:
        if '.' in e:
            first_level, next_level = e.split('.', 1)
            obj.first_level_expands.append(first_level)
            obj.next_level_expands.setdefault(first_level, []).append(next_level)
        else:
            obj.first_level_expands.append(e)
    obj.first_level_expands = list(set(obj.first_level_expands))

def initialize_explandable_serializer(obj, cls, *args, **kwargs):
    #don't pass the expand args up to the superclass
    obj.expand = kwargs.pop('expand', obj.expand if hasattr(obj, 'expand') else '')
    obj.first_level_expands = []
    obj.next_level_expands = {}

    # instantiate the superclass normally
    super(cls, obj).__init__(*args, **kwargs)

    if obj.expand and not obj.expandable_fields:
        raise ImproperExpandException

    obj.split_expands()

    for field in obj.first_level_expands:
        if field not in obj.expandable_fields:
            raise ImproperExpandException
        serializer, args, kwargs = obj.expandable_fields[field]
        if field in obj.next_level_expands:
            kwargs = dict(kwargs, **{'expand': obj.next_level_expands[field]})
        obj.fields[field] = serializer(*args, **kwargs)

class ExpandModelSerializer(serializers.HyperlinkedModelSerializer):
    """
        A ModelSerializer that uses the expand argument to figure out
        how to dynamically expand related fields.
    """

    split_expands = split_expands
    def __init__(self, *args, **kwargs):
        initialize_explandable_serializer(self, ExpandModelSerializer, *args, **kwargs)

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email') # 'snippets')

class ExtrasSerializer(ExpandModelSerializer):
    class Meta:
        model = SnippetExtra
        fields = ['extra_title',] 

    expandable_fields = {
                        'user': (UserSerializer, (), {'source': 'user'}),
                        }
    Meta.fields += expandable_fields.keys()

class SnippetSerializer(ExpandModelSerializer):
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ['url', 'highlight',
                  'title', 'code', 'linenos', 'language', 'style']

    expandable_fields = {
                        'owner': (UserSerializer, (), {'source': 'owner'}),
                        'extra': (ExtrasSerializer, (), {'source': 'extra'}),
                        }
    Meta.fields += expandable_fields.keys()
