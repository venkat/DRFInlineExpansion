from django.forms import widgets
from rest_framework import serializers
from snippets.models import Snippet, SnippetExtra, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    #snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail')

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

#class SnippetSerializer(serializers.HyperlinkedModelSerializer):
class SnippetSerializer(ExpandModelSerializer):
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')
    #owner = serializers.HyperlinkedIdentityField(view_name='user-detail')


    #Meta = type('Meta', (), {'model': Snippet, 'fields': ('url', 'highlight', 'title',)})
    class Meta:
        model = Snippet
        fields = ['url', 'highlight',
                  'title', 'code', 'linenos', 'language', 'style']

    expandable_fields = {
                        'owner': (UserSerializer, (), {'source': 'owner'}),
                        'extra': (ExtrasSerializer, (), {'source': 'extra'}),
                        }
    Meta.fields += expandable_fields.keys()
