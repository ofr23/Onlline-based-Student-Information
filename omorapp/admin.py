from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Student)
admin.site.register(Session)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(courseEvaluation)
admin.site.register(finalEvaluation)
admin.site.register(Mail)
admin.site.register(Notice)
admin.site.register(Attendance)
