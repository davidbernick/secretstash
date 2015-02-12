from django.shortcuts import render
from django.db import models
from django.http import Http404,HttpResponseNotAllowed, HttpResponseRedirect, HttpResponseForbidden, HttpResponseServerError, HttpResponse, HttpResponseRedirect
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
from .serializers import SecretSerializer,UserSerializer,HostSerializer,UserGroupSerializer
from .permissions import DjangoObjectPermissionsAll,DjangoModelPermissionsAll,DjangoObjectPermissionsChange
from guardian.shortcuts import assign_perm



def login_index(request, template_name='base.html'): #login default page. username/password box or create new user
        return render_to_response(template_name, {},context_instance=RequestContext(request))

def secret_index(request, template_name='signin.html'): #login default page. username/password box or create new user
        return render_to_response(template_name, {},context_instance=RequestContext(request))

class UserGroup(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    model=User
    def get_object(self, user):
        try:
            return User.objects.get(username=user)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, user, format=None):
        user = self.get_object(user)
        if not request.user.has_perm('secrets.change_host'):
            return HttpResponseForbidden()
        serializer = UserGroupSerializer(request.DATA,partial=True)

        try:
            action = serializer.data['action']
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        for group in serializer.data['groups']:
            if action=="add":
                try:
                    g = Group.objects.get(name=group)
                    if not request.user.has_perm('auth.change_group',g):
                     return HttpResponseForbidden()
                    user.groups.add(g)
                except Exception,e:
                    return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)

            elif action=="delete":
                try:
                    g = Group.objects.get(name=group)
                    if not request.user.has_perm('auth.change_group',g):
                     return HttpResponseForbidden()
                    user.groups.remove(g)
                except Exception,e:
                    return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)


class HostList(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    permission_classes = (DjangoModelPermissionsAll,)

class SecretList(viewsets.ModelViewSet):
    queryset = Secret.objects.all()
    serializer_class = SecretSerializer
    permission_classes = (DjangoObjectPermissionsChange,)
    filter_backends = (filters.DjangoFilterBackend,filters.DjangoObjectPermissionsFilter,)
    filter_fields = ('name',)
    
    def pre_save(self, obj):
        obj.owner = self.request.user

    def post_save(self, obj,created=True):
        for g in self.request.DATA['groups']:
            try:
                group = Group.objects.get(name=g)
                assign_perm('view_secret', group, obj)
                assign_perm('change_secret', group, obj)
                assign_perm('delete_secret', group, obj)
            except Exception,e:
                return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
