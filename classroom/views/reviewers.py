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

from ..decorators import teacher_required,student_required, reviewer_required
from ..forms import ReviewerSignUpForm
from ..models import Project, User, Course, Report, Comment
from django.core.mail import send_mail

class ReviewerSignUpView(CreateView):
    model = User
    form_class = ReviewerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'reviewer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        subject = "Welcome to Student Teacher Project Manager"
        message = "Your account has been created successfully. Now you can use our services.\nRegards\nStudent Teacher Project Manager"
        sender = "vichitrgandas@gmail.com"
        recipients=[user.email]
        #send_mail(subject,message,sender, recipients)
        login(self.request, user)
        return redirect('reviewer_home')

@method_decorator([ login_required, reviewer_required], name='dispatch')
class ReviewerHomePageView(ListView):
	model=Project
	ordering = ('name', )
	template_name='classroom/reviewers/home_page.html'
	context_object_name='projects'
	def get_queryset(self):
		#student = self.request.user
		#courses = student.courses.values_list('pk', flat=True)
		reviewer = self.request.user
		return reviewer.reviewer_projects.all

@login_required
@reviewer_required
def ProjectView(request, pk):
	project = Project.objects.get(pk=pk)
	course_id=int(project.courseid)
	reports = Report.objects.all().filter(projectid__exact=int(pk))
	return render(request, 'classroom/reviewers/project_page.html', context={'project':project,'reports':reports, 'course':course_id})

'''
@method_decorator([login_required, reviewer_required], name='dispatch')
class ProjectView(DetailView):
	model = Project
	template_name='classroom/reviewers/project_page.html'
	def view_project(request, pk):
		try:
			project = Project.objects.get(pk=pk)
			course_id = int(project.courseid)
			reports = Report.objects.all().filter(projectid__exact=course_id)
		except Project.DoesNotExist:
			raise Http404("Project does not exist")
		return render(request, 'classroom/reviewers/project_page.html', context={'project':project,'reports':reports, 'course':course_id})
'''

@method_decorator([login_required, reviewer_required], name='dispatch')	
class SubmitReview(UpdateView):
	model = Project
	fields = ('review',)
	
	template_name = 'classroom/reviewers/submit_review.html'
	#context_object_name='project'
	
	def form_valid(self, form):
		#course_id = int(self.kwargs.get('id'))
		project_id = int(self.kwargs.get('pk'))
		project= form.save(commit=False)
		#project.owner = self.request.user
		project.save()
		messages.success(self.request, 'The review was submitted successfully!')
		return redirect('project_page',project.pk )