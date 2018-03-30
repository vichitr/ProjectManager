from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import teacher_required,student_required
from ..forms import TeacherSignUpForm, AddStudentForm, AddReviewerForm
from ..models import Project, User, Course
from django.core.mail import send_mail

class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        subject = "Welcome to Student Teacher Project Manager"
        message = "Your account has been created successfully. Now you can use our services.\nRegards\nStudent Teacher Project Manager"
        sender = "vichitrgandas@gmail.com"
        recipients=[user.email]
        #send_mail(subject,message,sender, recipients)
        login(self.request, user)
        return redirect('my_courses')

@method_decorator([login_required, teacher_required], name='dispatch')
class AddStudentView(CreateView):
	model = User
	form_class = AddStudentForm
	template_name = 'classroom/teachers/add_student.html'
	#form_fields = ['username', 'password']
	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'student'
		return super().get_context_data(**kwargs)
	def form_valid(self, form):
		student = form.save()
		student.is_student = True
		return redirect('my_courses')
		
class AddReviewerView(CreateView):
	model = User
	form_class = AddReviewerForm
	template_name = 'classroom/teachers/add_reviewer.html'
	#form_fields = ['username', 'password']
	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'reviewer'
		return super().get_context_data(**kwargs)
	def form_valid(self, form):
		reviewer = form.save()
		reviewer.is_reviewer = True
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
class ProjectInfoView(DetailView):
	model = Course
	template_name='classroom/teachers/project_info.html'
	
	def project_info_view(request, pk):
		try:
			course_id = Course.objects.get(pk=pk)
		except Course.DoesNotExist:
			raise Http404("Course does not exist")
		return render(request, 'classroom/teachers/project_info.html',context={'course':course_id,})

@method_decorator([login_required, teacher_required], name='dispatch')
class UpdateProjectInfo(UpdateView):
	model = Course
	template_name = 'classroom/teachers/update_project_info.html'
	fields = ('project_details',)
		#template_name = 'classroom/teachers/course_update_form.html'
	context_object_name = 'course'
	def form_valid(self, form):
		course= form.save(commit=False)
		course.save()
		messages.success(self.request, 'Project info was updated successfully!')
		return redirect('project_info', course.pk)

@method_decorator([login_required], name='dispatch')
class CourseTeacherView(DetailView):
    model = Course
    template_name ='classroom/teachers/course_detail.html'
    '''
    context_object_name = 'course'
    def get_queryset(request, pk):
        course = Course.objects.get(pk=pk)
        return course
    '''

    def course_detail_view(request,pk):
        try:
            course_id=Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404("Course does not exist")

        #book_id=get_object_or_404(Book, pk=pk)

        return render(
            request,
            'classroom/teachers/course_detail.html',
            context={'course':course_id,}
        )

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
    fields = ('name','cls','semester','department','info')
    template_name = 'classroom/teachers/course_add_form.html'

    def form_valid(self, form):
        course= form.save(commit=False)
        course.owner = self.request.user
        course.save()
        messages.success(self.request, 'The course was added successfully!')
        return redirect('my_courses')

@method_decorator([login_required, teacher_required], name='dispatch')
class CourseUpdateView(UpdateView):
    model = Course
    fields = ('name','cls','semester','department','info')
    template_name = 'classroom/teachers/course_update_form.html'
    context_object_name = 'course'
    def form_valid(self, form):
        course= form.save(commit=False)
        course.owner = self.request.user
        course.save()
        messages.success(self.request, 'The course was updated successfully!')
        return redirect('course_teacher_page', course.pk)
