from django.contrib import admin

from .models.dentistreport_model import DentistReport
from .models.archivedreport_model import ArchivedDentistReport
from .models.auxiliary_models import DentistOfficeMessage


admin.site.register(DentistReport)
admin.site.register(ArchivedDentistReport)
admin.site.register(DentistOfficeMessage)
