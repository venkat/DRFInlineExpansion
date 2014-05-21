from rest_framework import viewsets


class ExpandModelMixin(object):
    """
        Apply this mixin to any view or viewset to dynamically generate the serializer_class
        which has the expand query parameter applied to the serializer
    """

    def get_serializer_class(self):
        if 'expand' in self.request.QUERY_PARAMS:
            expand = self.request.QUERY_PARAMS['expand']
            return type('Foo', (self.serializer_class,), {'expand': expand})
        return self.serializer_class

class ExpandModelViewSet(ExpandModelMixin, viewsets.ModelViewSet):
    pass
