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
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest import settings
from rest_framework.authentication import TokenAuthentication

# Create your views here.

def get_auth_token(request):
	"""
		Returns the token assigned to a particular 
		user instance, by passing the username and 
		password as part of the headers.
	"""
	username = request.POST.get('username')
	password = request.POST.get('password')
	user = authenticate(username=username, password=password)
	if user is not None:
		# the password verified for the user
		if user.is_active:
			token, created = Token.objects.get_or_create(user=user)
			request.session['auth'] = token.key
			return redirect('/polls/', request)
	return redirect(settings.LOGIN_URL, request)

@api_view(['GET'])
def api_root(request, format=None):
	"""
		API Endpoint with hyperlinks to user-list
		and snippet list. 
	"""
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
	"""
	API Endpoint that allows users to be viewed.
	"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	queryset = User.objects.all()
	serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
	"""
	API Endpoint that allows user detials to be viewed.
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer

class UpdateUserName(generics.UpdateAPIView):
	"""
		This class handles the update functionality
		for updating the username of a user.
		We pass the new username as part of header.
		command to run from command prompt: 
	curl -X PUT -H "Content-Type: application/json" -d '{"username": "Vikas"}' http://127.0.0.1:8080/user/update/3
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer
	
	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		instance.username = request.data.get('username')
		instance.save()

		serializer = self.get_serializer(instance, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)
		return Response(serializer.data)
	
class SnippetList(generics.ListCreateAPIView):
	"""
	API Endpoint that allows Snippet to be viewed.
	"""
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer
	
	def perform_create(self, serializer):
	    serializer.save(owner=self.request.user)	

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
	"""
	API Endpoint that allows Snippet detail to be viewed.
	"""
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
	statleness of data would be measured on some logic provided
	by the business people.
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
	"""
		Accepts two dates as arguments and 
		return the difference of days between
		them.
	"""
	d1 = datetime.strptime(d1, "%Y-%m-%d")
	d2 = datetime.strptime(d2, "%Y-%m-%d")
	return abs((d2 - d1).days)
