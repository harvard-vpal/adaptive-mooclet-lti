from rest_framework import viewsets
from .serializers import *
from rest_framework.decorators import detail_route
from rest_framework.response import Response

# rest framework viewsets
class MoocletViewSet(viewsets.ModelViewSet):
    queryset = Mooclet.objects.all()
    serializer_class = MoocletSerializer

    @detail_route()
    def test(self, request, pk=None):
    	return Response({'test':'hi'})

    @detail_route()
    def run(self, request, pk=None):
        policy = request.GET.get('policy',None)
    	version = self.get_object().run()
    	return Response(VersionSerializer(version).data)

class VersionViewSet(viewsets.ModelViewSet):
	queryset = Version.objects.all()
	serializer_class = VersionSerializer

class VariableViewSet(viewsets.ModelViewSet):
	queryset = Variable.objects.all()
	serializer_class = VariableSerializer

class ValueViewSet(viewsets.ModelViewSet):
	queryset = Value.objects.all()
	serializer_class = ValueSerializer

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
