from django.contrib import admin
from .models import *

admin.site.register(PasswordReset)

admin.site.register(State)
admin.site.register(District)
admin.site.register(Block)
admin.site.register(School)
admin.site.register(Teacher)
admin.site.register(Record)
admin.site.register(School_teacher)
