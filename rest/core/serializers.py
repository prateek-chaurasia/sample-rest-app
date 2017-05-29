from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest.core.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class UserSerializer(serializers.ModelSerializer):
	"""
		This serializes the data of User model and transforms 
		it to JSON format. Snippet field will be a hyperlink
		to the actual snippet instance in the Snippet model.
	"""
	snippets = serializers.HyperlinkedRelatedField(
					many=True,
					view_name='snippet-detail', 
					read_only=True
				)
	class Meta:
		model = User
		fields = ('url', 'id', 'username', 'snippets')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
	"""
		This serializes the data of Group model and transforms 
		it to JSON format.
	"""
	class Meta:
		model = Group
		fields = ('url', 'name')

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
	"""
		This serializes the data of Snippet model and transforms 
		it to JSON format. Owner will be a readonly field with
		the username of the user, and highlight will be a
		highlighted filed.
	"""
	owner = serializers.ReadOnlyField(source='owner.username')
	highlight = serializers.HyperlinkedIdentityField(
					view_name='snippet-highlight', 
					format='html'
					)
	class Meta:
		model = Snippet
		fields = ('url', 'id', 'highlight', 'owner', 'title', 
					'code', 'linenos', 'language', 'style'
					)





