"""ProjectManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from classroom.views import classroom, students, teachers, reviewers
#from django.contrib.staticfiles.urls import static
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
	path('me/', admin.site.urls),
	path('', include('classroom.urls')),
	path('accounts/',include('django.contrib.auth.urls')),
	path('accounts/signup/', classroom.SignUpView.as_view(), name='signup'),
	path('accounts/profile/', classroom.ProfileView.as_view(), name='profile'),
	path('accounts/<int:pk>/profile/update/', classroom.ProfileUpdateView.as_view(), name='update_profile'),
	path('accounts/signup/student',students.StudentSignUpView.as_view(), name='student_signup'),
	path('accounts/signup/teacher',teachers.TeacherSignUpView.as_view(), name='teacher_signup'),
	path('accounts/signup/reviewer',reviewers.ReviewerSignUpView.as_view(), name='reviewer_signup'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)