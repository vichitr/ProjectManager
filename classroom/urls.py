from django.urls import include, path
from django.conf.urls import url

from .views import classroom, students, teachers, reviewers

urlpatterns = [
	path('', classroom.home, name='home'),
	path('classroom/courses/', students.CourseListView.as_view(), name='student_courses'),
	path('classroom/mycourses/', teachers.MyCourseListView.as_view(), name='my_courses'),
	path('classroom/mycourses/add/', teachers.CourseCreateView.as_view(), name='add_course'),
	path('reviewers/home/', reviewers.ReviewerHomePageView.as_view(), name='reviewer_home'),
	path('classroom/courses/<int:pk>/', students.CoursePageView.as_view(), name='course_page'),
	path('classroom/mycourses/<int:pk>/', teachers.CourseTeacherView.as_view(), name='course_teacher_page'),
	path('classroom/mycourses/<int:pk>/update/', teachers.CourseUpdateView.as_view(), name='update_course'),
	path('classroom/add/student/', teachers.AddStudentView.as_view(), name='add_student'),
	path('classroom/add/reviewer/', teachers.AddReviewerView.as_view(), name='add_reviewer'),
	
]
