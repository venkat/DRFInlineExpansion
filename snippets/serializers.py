from django.contrib.auth.models import User
from django.forms import widgets
from rest_framework import serializers
from rest_framework.exceptions import APIException

from snippets.models import Snippet, SnippetExtra, LANGUAGE_CHOICES, STYLE_CHOICES

from expand.serializers import HyperlinkedExpandModelSerializer

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email')

class ExtrasSerializer(HyperlinkedExpandModelSerializer):
    class Meta:
        model = SnippetExtra
        fields = ['extra_title',] 

    expandable_fields = {
                        'user': (UserSerializer, (), {'source': 'user'}),
                        }
    Meta.fields += expandable_fields.keys()

class SnippetSerializer(HyperlinkedExpandModelSerializer):
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
