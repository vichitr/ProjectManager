from django.test import TestCase
from .forms import TeacherSignUpForm, AddStudentForm, AddReviewerForm, CommentForm, AssignReviewerForm,StudentSignUpForm, ProjectCreationForm, ReportForm,ReviewerSignUpForm
from .models import Project, User, Course, Comment, Report, Teacher, Student
from .views import classroom, students, teachers, reviewers
