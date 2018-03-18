from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import teacher_required,student_required
from ..forms import IdeaForm, TeacherSignUpForm
from ..models import Solution, Idea, Project, User, Subject, Course


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('my_courses')

@method_decorator([login_required], name='dispatch')
class MyCourseListView(ListView):
	model=Course
	ordering=('name',)
	context_object_name = 'my_courses'
	template_name = 'classroom/teachers/my_courses.html'
	
	def get_queryset(self):
		teacher = self.request.user
		courses = teacher.courses.all
		return courses

	
@method_decorator([login_required], name='dispatch')
class ProjectListView(ListView):
    model = Project
    ordering = ('name', )
    context_object_name = 'projects'
    template_name = 'classroom/teachers/course_update_list.html'

    def get_queryset(self):
        queryset = self.request.user.projects \
            .select_related('subject') \
            .annotate(ideas_count=Count('ideas', distinct=True)) \
            .annotate(taken_count=Count('taken_projects', distinct=True))
        return queryset


@method_decorator([login_required, teacher_required], name='dispatch')
class CourseCreateView(CreateView):
    model = Course
    fields = ('name', 'info', )
    template_name = 'classroom/teachers/course_add_form.html'

    def form_valid(self, form):
        course= form.save(commit=False)
        course.owner = self.request.user
        course.save()
        messages.success(self.request, 'The course was added successfully! Go ahead and add some information now.')
        return redirect('my_courses')


@method_decorator([login_required, student_required], name='dispatch')
class IdeaDeleteView(DeleteView):
    model = Idea
    context_object_name = ''
    template_name = 'classroom/students/idea_delete_confirm.html'
    pk_url_kwarg = 'idea_pk'

    def get_context_data(self, **kwargs):
        course = self.get_object()
        kwargs['idea'] = idea.project
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        idea = self.get_object()
        messages.success(request, 'The idea %s was deleted successfully!' % idea.text)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Idea.objects.filter(project__owner=self.request.user)

    def get_success_url(self):
        idea = self.get_object()
        return reverse('students:project_update', kwargs={'pk': idea.project_id})