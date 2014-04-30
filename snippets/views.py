from snippets.models import Snippet, SnippetExtra
from snippets.serializers import SnippetSerializer, ExtrasSerializer
from django.http import Http404
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from snippets.serializers import UserSerializer
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework.response import Response



from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly


from rest_framework import viewsets
from rest_framework.decorators import link

class ExpandModelMixin(object):
    """
        Apply this mixin to any view or viewset to dynamically generate the serializer_class
        which has the expand parameter applied to the class
    """

    def get_serializer_class(self):
        if 'expand' in self.request.QUERY_PARAMS:
            expand = self.request.QUERY_PARAMS['expand']
            print "expand QUERY_PARAMS", expand, "class name", self.serializer_class.__name__
            return type('Foo', (self.serializer_class,), {'expand': expand})
            #self.serializer_class.expand = expand
        return self.serializer_class

class ExpandModelViewSet(ExpandModelMixin, viewsets.ModelViewSet):
    pass


class SnippetViewSet(ExpandModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @link(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def pre_save(self, obj):
        obj.owner = self.request.user


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SnippetExtraViewSet(viewsets.ModelViewSet):
     queryset = SnippetExtra.objects.all()
     serializer_class = ExtrasSerializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

     def pre_save(self, obj):
        obj.user = self.request.user

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format),
        'extras': reverse('snippetextra-list', request=request, format=format),
    })


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
