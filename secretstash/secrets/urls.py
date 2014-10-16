from django.conf.urls import patterns, include, url
from django.contrib.auth import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import SecretList,HostList,UserGroup
from rest_framework.routers import DefaultRouter
from rest_framework import renderers


router = DefaultRouter()
router.register(r'secret', SecretList)
router.register(r'host', HostList)

urlpatterns = patterns(
                       'secrets.views',
                       url(r'^logout/$', views.logout, {'next_page':'/secrets/'},name='logout'),
                       url(r'^$', 'secret_index', {'template_name':'signin.html'}, name='secret_index'),
                       url(r'^usergroup/(?P<user>.*)/$', UserGroup.as_view()),                                              
                       url(r'^api/', include(router.urls)),
)

