from rest_framework import serializers

from expand.utils import split_expands, initialize_explandable_serializer

class ExpandModelSerializer(serializers.ModelSerializer):
    """
        A ModelSerializer that uses the expand argument to figure out
        how to dynamically expand related fields.
    """

    def __init__(self, *args, **kwargs):
        initialize_explandable_serializer(self, ExpandModelSerializer, *args, **kwargs)


class HyperlinkedExpandModelSerializer(serializers.HyperlinkedModelSerializer):
    """
        A HyperlinkedModelSerializer that uses the expand argument to figure out
        how to dynamically expand related fields.
    """

    def __init__(self, *args, **kwargs):
        initialize_explandable_serializer(self, HyperlinkedExpandModelSerializer, *args, **kwargs)
