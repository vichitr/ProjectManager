from django.contrib import admin
from classroom.models import Project, Student, User, Course,Teacher, Comment, Report

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
            'fields': ('username','first_name','last_name','email','phone_number', 'password','is_student','is_teacher','is_reviewer',)
        }),
    )
admin.site.register(User, UserAdmin)

class TeacherAdmin(admin.ModelAdmin):
	fieldsets=(
		(None, {
			'fields':('user','courses',)
		}),
	)
admin.site.register(Teacher, TeacherAdmin)

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
            'fields': ('courseid', 'title', 'owner','members','idea','review','reviewee','marks_assigned','marks',)
        }),
    )
admin.site.register(Project, ProjectAdmin)

class CommentAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('project','author','text','created_date',)
		}),
	)
admin.site.register(Comment, CommentAdmin)

class RepoerAdmin(admin.ModelAdmin):
	fieldsets=(
		(None, {
			'fields': ('file', 'projectid',)
		}),
	)
admin.site.register(Report, RepoerAdmin)