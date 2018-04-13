from django.urls import include, path
from django.conf.urls import url

from .views import classroom, students, teachers, reviewers

urlpatterns = [
	path('', classroom.home, name='home'),
	path('classroom/courses/', students.CourseListView.as_view(), name='student_courses'),
	path('classroom/mycourses/', teachers.MyCourseListView.as_view(), name='my_courses'),
	path('classroom/mycourses/add/', teachers.CourseCreateView.as_view(), name='add_course'),
	path('reviewers/home/', reviewers.ReviewerHomePageView.as_view(), name='reviewer_home'),
	path('reviewers/home/projects/<int:pk>/', reviewers.ProjectView, name='project_page'),
	path('reviewers/home/projects/<int:pk>/review/', reviewers.SubmitReview.as_view(), name='submit_review'),
	path('classroom/courses/<int:pk>/', students.CoursePageView.as_view(), name='course_page'),
	path('classroom/courses/<int:pk>/submitted_projects', students.SubmittedProjectsView.as_view(), name='submitted_projects'),
	path('classroom/courses/<int:pk>/project_info/', students.ProjectInfoView.as_view(), name='project_detail'),
	path('classroom/courses/<int:pk>/myproject/', students.MyProjectView.as_view(), name='my_project'),
	path('classroom/courses/<int:pk>/myproject/submit/', students.SubmitMyProjectView.as_view(), name='submit_my_project'),
	path('classroom/courses/course/<int:pk>/submit_report/', students.SubmitReport, name='submit_report'),
	path('classroom/courses/course/<int:pk>/update/', students.UpdateMyProjectView.as_view(), name='update_my_project'),
	path('classroom/mycourses/<int:pk>/', teachers.CourseTeacherView.as_view(), name='course_teacher_page'),
	path('classroom/mycourses/<int:pk>/submitted_projects', teachers.SubmittedProjectsView.as_view(), name='submitted_course_projects'),
	path('classroom/mycourses/course/submitted_projects/<int:pk>/', teachers.ViewProjectView, name='view_project'),
	path('classroom/mycourses/course/submitted_projects/<int:pk>/assign_marks/', teachers.AssignMarks.as_view(), name='assign_marks'),
	path('classroom/mycourses/course/submitted_projects/<int:pk>/assign_reviewer/', teachers.AssignReviewer, name='assign_reviewer'),
	path('classroom/mycourses/course/submitted_projects/<int:pk>/post_comment', teachers.PostComment, name='post_comment'),
	path('classroom/mycourses/<int:pk>/project_info/', teachers.ProjectInfoView.as_view(), name='project_info'),
	path('classroom/mycourses/<int:pk>/project_info/update/', teachers.UpdateProjectInfo.as_view(), name='update_project_info'),
	path('classroom/mycourses/<int:pk>/update/', teachers.CourseUpdateView.as_view(), name='update_course'),
	path('classroom/add/student/', teachers.AddStudentView.as_view(), name='add_student'),
	path('classroom/add/reviewer/', teachers.AddReviewerView.as_view(), name='add_reviewer'),
	
]
