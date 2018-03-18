from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from ..decorators import student_required
from ..forms import StudentCoursesForm, StudentSignUpForm, TakenProjectForm, IdeaForm
from ..models import Project, Student, TakenProject, User, Course


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('student_courses')


@method_decorator([login_required, student_required], name='dispatch')
class CourseListView(ListView):
	model=Course
	ordering = ('name', )
	template_name='classroom/students/student_courses.html'
	context_object_name='courses'
	def get_queryset(self):
		#student = self.request.user
		#courses = student.courses.values_list('pk', flat=True)
		return Course.objects.all

@method_decorator([login_required, student_required], name='dispatch')
class ProjectListView(ListView):
    model = Project
    ordering = ('name', )
    context_object_name = 'projects'
    template_name = 'classroom/students/project_list.html'

    def get_queryset(self):
        student = self.request.user.student
        student_courses = student.courses.values_list('pk', flat=True)
        taken_projects = student.projects.values_list('pk', flat=True)
        queryset = Project.objects.filter(subject__in=student_courses) 
           # .exclude(pk__in=taken_quizzes) \
            #.annotate(questions_count=Count('questions')) \
            #.filter(_count__gt=0)
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class TakenProjectListView(ListView):
    model = TakenProject
    context_object_name = 'taken_projects'
    template_name = 'classroom/students/taken_project_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_projects \
            .select_related('project', 'project__subject') \
            .order_by('project__name')
        return queryset
