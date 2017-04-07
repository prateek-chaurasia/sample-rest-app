from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest.core import views

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^snippets/$', views.SnippetList.as_view(), 
		name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)$', 
		views.SnippetDetail.as_view(), 
		name='snippet-detail'),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', 
		views.SnippetHighlight.as_view(),
		name='snippet-highlight'),
	url(r'^users/$', views.UserList.as_view(),
		name='user-list'),
	url(r'^users/(?P<pk>[0-9]+)/$', 
		views.UserDetail.as_view(),
		name='user-detail'),
    url(r'^snippets/status/v1/$', views.SnippetFreshnessView.as_view(), 
		name='snippet-freshness-v1'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
