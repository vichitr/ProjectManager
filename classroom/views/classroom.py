from django.shortcuts import redirect, render
from django.views.generic import TemplateView


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