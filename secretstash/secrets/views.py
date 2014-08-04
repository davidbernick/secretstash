from django.shortcuts import render
from django.db import models
from django.http import HttpResponseNotAllowed, HttpResponseRedirect, HttpResponseForbidden, HttpResponseServerError, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Q
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import logout,authenticate, login
from django.contrib.sites.models import Site
from django.core.files.storage import default_storage

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.admin.sites import site
from django.template import RequestContext, loader

from rest_framework import status,filters,viewsets
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from .models import Host,Secret
from .serializers import SecretSerializer,UserSerializer,HostSerializer
from .permissions import DjangoObjectPermissionsAll,DjangoModelPermissionsAll
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def login_index(request, template_name='base.html'): #login default page. username/password box or create new user
        return render_to_response(template_name, {},context_instance=RequestContext(request))

def secret_index(request, template_name='signin.html'): #login default page. username/password box or create new user
        return render_to_response(template_name, {},context_instance=RequestContext(request))

class HostList(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    permission_classes = (DjangoModelPermissionsAll,)
    
    def pre_save(self, obj):
        obj.owner = self.request.user

class SecretList(viewsets.ModelViewSet):
    queryset = Secret.objects.all()
    serializer_class = SecretSerializer
    filter_backends = (filters.DjangoObjectPermissionsFilter,)
    permission_classes = (DjangoObjectPermissionsAll,)
    
    def pre_save(self, obj):
        obj.owner = self.request.user