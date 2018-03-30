from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView, TemplateView
from django.core.mail import send_mail
from ..decorators import student_required
from ..forms import StudentSignUpForm, ProjectCreationForm
from ..models import Project, Student, User, Course


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        subject = "Welcome to Student Teacher Project Manager"
        message = "Your account has been created successfully. Now you can use our services.\nRegards\nStudent Teacher Project Manager"
        sender = "vichitrgandas@gmail.com"
        recipients=[user.email]
        #send_mail(subject,message,sender, recipients)
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

@method_decorator([login_required], name='dispatch')
class CoursePageView(DetailView):
    model = Course
    template_name ='classroom/students/course_page.html'
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
            'classroom/students/course_page.html',
            context={'course':course_id,}
        )

@method_decorator([login_required], name='dispatch')
class ProjectInfoView(DetailView):
	model = Course
	template_name='classroom/students/project_info.html'
	
	def project_info_view(request, pk):
		try:
			course_id = Course.objects.get(pk=pk)
		except Course.DoesNotExist:
			raise Http404("Course does not exist")
		return render(request, 'classroom/students/project_info.html',context={'course':course_id,})

@method_decorator([login_required],name='dispatch')
class SubmittedProjectsView(ListView):
	#model = Course
	template_name = 'classroom/students/submitted_projects.html'
	#queryset = Project.objects.all()
	context_object_name = 'projects'
	#ordering = ('name', )
	#projects = []
	
	def get_queryset(self):
		#course = Course.objects.get(pk=self.kwargs.get('pk'))
		projects = Project.objects.all().filter(courseid__exact=int(self.kwargs.get('pk')))
		return projects
	
	def get_context_data(self, **kwargs):
		context = super(SubmittedProjectsView, self).get_context_data(**kwargs)
		course = Course.objects.get(pk=self.kwargs.get('pk'))
		context['course']=course
		return context
	'''
	def submitted_projects_view(self, request, pk):
		#course_id = self.kwargs.get('pk')
		#pros=Project.objects.all
		#projects = [pro for pro in pros if pro.courseid == course_id]
		#courses = student.courses.values_list('pk', flat=True)
		#projects = Project.objects.all() #.filter(courseid__exact = course_id)
		#return projects
		try:
			course = Course.objects.get(pk=pk)
			student = self.request.user
			projects =Project.objects.all  #filter(courseid__exact=pk)
		except Course.DoesNotExist:
			raise Http404("Course does not exist")
		return render(request, 'classroom/students/submitted_projects.html',context={'course':course,'projects':projects})
	'''
	
@method_decorator([login_required, student_required], name='dispatch')
class MyProjectView(ListView):
	#model = Course
	template_name = 'classroom/students/my_project.html'
	context_object_name='projects'
	def get_queryset(self):
		#course = Course.objects.get(pk=self.kwargs.get('pk'))
		projects = Project.objects.all().filter(courseid__exact=int(self.kwargs.get('pk')))
		return projects
	
	def get_context_data(self, **kwargs):
		context = super(MyProjectView, self).get_context_data(**kwargs)
		course = Course.objects.get(pk=self.kwargs.get('pk'))
		context['course']=course
		pros = Project.objects.all().filter(courseid__exact=int(self.kwargs.get('pk')))
		if len(pros)!=0:
			project = pros[0]
			for i in pros:
				if i.owner==self.request.user:
					project = i
					break
			context['project']=project
		else:
			context['project']=None
		'''
		pros = Project.objects.all().filter(courseid__exact=int(self.kwargs.get('pk')))
		project = pros[0]
		for i in pros:
			if i.owner == self.request.user:
				project = i
				break
		context['project'] = project
		'''
		return context
	'''
	def myproject_view(self, request, pk):
		#course = Course.objects.get(pk=pk)
		#project = course.projects.filter(owner=self.request.user)
		try:
			course = Course.objects.get(pk=pk)
			student = self.request.user
			projects =Project.objects.filter(courseid__exact=int(pk))
			project = projects[0]
			for i in projects:
				if i.owner == request.user:
					project = i
					break
		except Course.DoesNotExist:
			raise Http404("Course does not exist")
		return render(request, 'classroom/students/my_project.html',context={'course':course,'project':project, 'projects':projects})
	'''
	
@method_decorator([login_required, student_required], name='dispatch')		
class SubmitMyProjectView(CreateView):
	model = Project
	form_class = ProjectCreationForm
	#fields = ('title','members','idea',)
	template_name = 'classroom/students/submit_my_project.html'
	#context_object_name='course'
	#course = Course()
	
	def form_valid(self, form):
		project= form.save(commit=False)
		project.owner = self.request.user
		project.courseid = self.kwargs.get('pk')
		project.save()
		messages.success(self.request, 'The project was submitted successfully!')
		course=Course.objects.get(pk=self.kwargs.get('pk'))
		#context={'course':course}
		return redirect('my_project', course.pk)
	def get_context_data(self, **kwargs):
		context = super(SubmitMyProjectView, self).get_context_data(**kwargs)
		course=Course.objects.get(pk=self.kwargs.get('pk'))
		context['course']=course
		return context
		'''
	def myproject_submit(request, pk):
		try:
			course=Course.objects.get(pk=pk)
		except Course.DoesNotExist:
			raise Http404("Course does not exist")
		return redirect('my_project', context = {'course':course})
		'''

@method_decorator([login_required, student_required], name='dispatch')	
class UpdateMyProjectView(UpdateView):
	model = Project
	fields = ('title','members','idea',)
	'''
	emplate_name = 'classroom/students/submit_my_project.html'
	context_object_name='project'
	
	def form_valid(self, form):
		project= form.save(commit=False)
		project.owner = self.request.user
		project.save()
		messages.success(self.request, 'The project was submitted successfully!')
		return redirect('my_project')
	'''	
	
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
