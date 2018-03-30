from django.shortcuts import redirect, render
from django.views.generic import TemplateView, UpdateView
from ..models import  User
from django.contrib import messages

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('my_courses')
        elif request.user.is_reviewer:
            return redirect('reviewer_home')
        else:
            return redirect('student_courses')
    return render(request, 'classroom/home.html')

class ProfileView(TemplateView):
	template_name = 'classroom/profile.html'
	
class ProfileUpdateView(UpdateView):
	model = User
	fields = ('first_name','last_name','email','phone_number')
	template_name = 'classroom/profile_update_form.html'
	def form_valid(self, form):
		user = form.save(commit=False)
		user.save()
		messages.success(self.request, 'Profile has been updated successfully!')
		return redirect('profile')