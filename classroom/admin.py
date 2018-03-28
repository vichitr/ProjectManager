from django.contrib import admin
from classroom.models import Project, Student, TakenProject, User, Course,Solution, Idea, Subject

class StudentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password',)
        }),
    )

admin.site.register(Student, StudentAdmin)
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('username','first_name','last_name','email', 'password','is_student','is_teacher','is_reviewer',)
        }),
    )
admin.site.register(User, UserAdmin)
class CourseAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'info','owner',)
        }),
    )

admin.site.register(Course, CourseAdmin)

class ProjectAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'subject','owner',)
        }),
    )

admin.site.register(Project, ProjectAdmin)

