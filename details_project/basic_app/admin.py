from django.contrib import admin
from basic_app.models  import UserInfo,audit
admin.site.register(UserInfo)
admin.site.register(audit)
# Register your models here.
#make migrations whenever models register
