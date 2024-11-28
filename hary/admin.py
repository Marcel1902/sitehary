from django.contrib import admin
from .models import Activity, Event, Blog
from  django.utils.translation import gettext_lazy as _

# Register your models here.
admin.site.register(Activity)
admin.site.register(Event)
admin.site.register(Blog)

admin.site.site_title = _("H'ARY")
admin.site.site_header = _('Hary Administration')
admin.site.index_title = _('Welcome to Hary Administration')
