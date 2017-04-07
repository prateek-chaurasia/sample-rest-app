from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest.core.serializers import UserSerializer, GroupSerializer, SnippetSerializer
from rest_framework import viewsets, status, mixins, generics, permissions, renderers
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest.core.models import Snippet
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest.core.permissions import IsOwnerOrReadOnly
from datetime import datetime

# Create your views here.

@api_view(['GET'])
def api_root(request, format=None):
	return Response({
			'users': reverse('user-list', request=request, format=format),
			'snippets': reverse('snippet-list', request=request, format=format)
			})
	

class UserViewSet(viewsets.ModelViewSet):
	"""
	API Endpoint that allows users to be viewed or edited.
	"""
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
	"""
	API Endpoint that allows group to be viewed or edited.
	"""
	queryset = Group.objects.all()
	serializer_class = GroupSerializer

class UserList(generics.ListAPIView):
#	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	queryset = User.objects.all()
	serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class SnippetList(generics.ListCreateAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer
	
	def perform_create(self, serializer):
	    serializer.save(owner=self.request.user)	


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
							IsOwnerOrReadOnly)
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer

class SnippetHighlight(generics.GenericAPIView):
	queryset = Snippet.objects.all()
	rendered_classes = (renderers.StaticHTMLRenderer,)

	def get(self, request, *args, **kwargs):
		snippet = self.get_object()
		return Response(snippet.highlighted)

class SnippetFreshnessView(APIView):
	"""
	A view that returns status of staleness of data in JSON.
	statleness of data would be measured on some logic.
	"""
	renderer_classes = (JSONRenderer,)

	def get(self, request, format=None):
		last_entry_obj = Snippet.objects.latest('created')
		last_entry_date = datetime.strftime(last_entry_obj.created, "%Y-%m-%d")
		current_date = datetime.strftime(datetime.now(), "%Y-%m-%d")
		diff_days = days_between(last_entry_date, current_date)
		if diff_days >= 7:
			status = "stale"
		elif diff_days < 7:
			status = "fresh"
		content = [{'staleness_count': diff_days,
					'status': status}]
		return Response(content)


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)
