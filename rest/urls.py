"""rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest.core import views
from rest.core import urls as URLS
from rest_framework.authtoken import views as rest_framework_views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
#	url(r'^', include(router.urls)),
	url(r'^', include(URLS)),
#	url(r'^login/$', views.get_auth_token, name='login'),
#    url(r'^logout/$', views.logout_user, name='logout'),
#    url(r'^auth/$', views.login_form, name='login_form'),
	url(r'^get_auth_token$', rest_framework_views.obtain_auth_token, name='get_auth_token'),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
