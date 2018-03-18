from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_reviewer = models.BooleanField(default=False)

		
class Subject(models.Model):
    name = models.CharField(max_length=30)
    subject=models.CharField(max_length = 100)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)

class Course(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
	#invloved_students = models.ManyToManyField(User, related_name='students')
	name = models.CharField(max_length=500)
	#projects = models.ManyToManyField(Project, on_delete=models.CASCADE, related_name='projects_list')
	info = models.CharField(max_length=100000)
	
	def __str__(self):
		return self.name

class Teacher(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	courses = models.ManyToManyField(Course,  related_name='my_courses')
	def __str__(self):
		return self.user.username

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students')
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.name

class Idea(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ideas')
    text = models.CharField('Idea', max_length=255)

    def __str__(self):
        return self.text


class Solution(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='solutions')
    text = models.CharField('Solution', max_length=255)
    #is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    projects = models.ManyToManyField(Project, through='TakenProject')
    courses = models.ManyToManyField(Course, related_name='courses')

    def get_uncompleted_projects(self, project):
        completed_projects = self.course.projects \
            .filter(solution__idea__project=project) \
            .values_list('solution__idea__pk', flat=True)
        ideas = project.ideas.exclude(pk__in=completed_projects).order_by('text')
        return ideas

    def __str__(self):
        return self.user.username


class TakenProject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_projects')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='taken_projects')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class StudentSolution(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='project_solutions')
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='solutions')
