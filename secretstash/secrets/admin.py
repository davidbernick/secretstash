from django.contrib import admin
from .models import Secret,Host
from guardian.admin import GuardedModelAdmin
from django.contrib.auth.models import User, Group, Permission


class SecretAdmin(GuardedModelAdmin):
    pass

class HostAdmin(GuardedModelAdmin):
    pass

class GroupAdmin(GuardedModelAdmin):
    pass

admin.site.register(Secret,SecretAdmin)
admin.site.register(Host,HostAdmin)
admin.site.register(Group,GroupAdmin)
