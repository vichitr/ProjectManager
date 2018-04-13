from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from django.db import models
from django.utils.html import escape, mark_safe
from django.utils import timezone
import datetime

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)
	
class User(AbstractUser):
	is_student = models.BooleanField(default=False)
	is_teacher = models.BooleanField(default=False)
	is_reviewer = models.BooleanField(default=False)
	image = models.ImageField(upload_to =user_directory_path, default='user.png')
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
	assigned_projects = models.IntegerField(default=0)
	#phone_number=PhoneNumberField( blank=True,  default='0')

class Report(models.Model):
	file = models.FileField(upload_to='uploads/' )
	projectid = models.IntegerField(default=0)

class Project(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
	title = models.CharField(max_length=500)
	members=models.CharField(max_length=200)
	idea = models.CharField(max_length=1000000, default='')
	review=models.CharField(max_length= 1000000, default='')
	#comments=models.CharField(max_length=1000000, default='')
	marks_assigned = models.BooleanField(default=False)
	marks = models.IntegerField(default=0)
	courseid = models.IntegerField(default = 0)
	is_assigned = models.BooleanField(default=False)
	#reviewee_choices = User.objects.filter(is_reviewer=True)
	#reviewees = models.CharField(max_length=1, choices=reviewee_choices)
	reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'reviewer_projects')
    #subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='projects')

	def __str__(self):
		return self.title
	def members_as_list(self):
		m = list(map(str, self.members.split(',')))
		return m

class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    #approved_comment = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Course(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
	#invloved_students = models.ManyToManyField(User, related_name='students')
	name = models.CharField(max_length=500)
	classes=(
		('a', 'B. Tech'),
		('b', 'M. Tech'),
		('c', 'MCA'),
		('d',  'PhD'),
	)
	cls = models.CharField(max_length=1, choices=classes)
	sems =(
		('1',  '1'),
		('2',  '2'), 
		('3',  '3'), 
		('4',  '4'), 
		('5', '5'), 
		('6', '6'), 
		('7', '7'), 
		('8', '8'),
	)
	semester = models.CharField(max_length=1, choices=sems)
	deps = (
		('a', 'Department of Computer Science and Engineering'),
		('b', 'Department of Information Technology'),
		('c', 'Department of Electronics & Communication Engineering'),
		('d',  'Department of Electrical and Electronics Engineering'),
		('e', 'Department of Mechanical Engineering'),
		('f', 'Department of Civil Engineering'),
		('g', 'Department of Mathematical and Computational Sciences'),
		('h', 'Department of Mining Engineering'),
		('i', 'Department of Chemical Engineering'),
		('j', 'Department of Metallurgical and Materials Engineering'),
		('k', 'Department of Applied Mechanics and Hydraulics'),
		('l', 'Department of Physics'),
		('m', 'Department of Chemistry'),
		('n', 'Department of Placement and Training'),
		('o', 'School of Management'),
	)
	department = models.CharField(max_length=1, choices = deps)
	#projects = models.ManyToManyField(Project, on_delete=models.CASCADE, related_name='projects_list')
	info = models.CharField(max_length=100000)
	project_details = models.CharField(max_length=1000000, default='')
	#projects = models.ManyToManyField(Project, related_name='course_projects')
	def __str__(self):
		return self.name

class Teacher(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	courses = models.ManyToManyField(Course,  related_name='my_courses')
	def __str__(self):
		return self.user.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    projects = models.ManyToManyField(Project, related_name='myprojects')
    #courses = models.ManyToManyField(Course, related_name='courses')

    def __str__(self):
        return self.user.username

		