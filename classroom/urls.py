from django.urls import include, path
from django.conf.urls import url

from .views import classroom, students, teachers, reviewers

urlpatterns = [
	path('', classroom.home, name='home'),
	path('students/courses/', students.CourseListView.as_view(), name='student_courses'),
	path('teachers/mycourses/', teachers.MyCourseListView.as_view(), name='my_courses'),
	path('teachers/mycourses/add/', teachers.CourseCreateView.as_view(), name='add_course'),
	path('reviewers/home/', reviewers.ReviewerHomePageView.as_view(), name='reviewer_home'),
]
