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
from ..models import Project, User, Course
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

class ReviewerHomePageView(ListView):
	model=Project
	ordering = ('name', )
	template_name='classroom/reviewers/home_page.html'
	context_object_name='projects'
	def get_queryset(self):
		#student = self.request.user
		#courses = student.courses.values_list('pk', flat=True)
		return Project.objects.all

