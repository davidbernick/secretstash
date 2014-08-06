from django.contrib import admin
from .models import Secret,Host
from guardian.admin import GuardedModelAdmin

class SecretAdmin(GuardedModelAdmin):
    pass

class HostAdmin(GuardedModelAdmin):
    pass

admin.site.register(Secret,SecretAdmin)
admin.site.register(Host,HostAdmin)