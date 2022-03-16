from django.contrib import admin

# Register your models here.
from .models import User, Learner, Course, Announcements

admin.site.register(User)
admin.site.register(Learner)
admin.site.register(Course)
admin.site.register(Announcements)
