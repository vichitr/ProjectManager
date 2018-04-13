from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from classroom.models import Student, Course, Project, User, Comment, Report


class TeacherSignUpForm(UserCreationForm):
    first_name =  forms.CharField( max_length=100, required=True)
    email = forms.EmailField(required=True)
   # phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', required=False)
    #contact_no=PhoneNumberField()
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','phone_number' ]
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user

class ReviewerSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length= 254, required=True)
    first_name= forms.CharField(max_length=50, required=True)
   # phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', required=False)
    #contact_no=PhoneNumberField()
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','phone_number']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_reviewer = True
        if commit:
            user.save()
        return user

class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length= 254, required=True)
    first_name= forms.CharField(max_length=50, required=True)
    #phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', required=False)
    #contact_no=PhoneNumberField()
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        #student = Student.objects.create(user=user)
        #student.courses.add(*self.cleaned_data.get('courses'))
        return user

class AddStudentForm(UserCreationForm):
    #email = forms.EmailField(max_length= 254, required=True)
    #first_name= forms.CharField(max_length=50, required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        #fields = ['username', 'first_name', 'last_name', 'email', ]
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        #student = Student.objects.create(user=user)
        #student.courses.add(*self.cleaned_data.get('courses'))
        return user

class AddReviewerForm(UserCreationForm):
    #email = forms.EmailField(max_length= 254, required=True)
    #first_name= forms.CharField(max_length=50, required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        #fields = ['username', 'first_name', 'last_name', 'email', ]
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_reviewer = True
        if commit:
            user.save()
        return user		

class ProjectCreationForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['title','members','idea']
		widgets={
			'members': forms.TextInput(attrs={'placeholder':'Member names separated by commas'}),
			'idea': forms.Textarea(attrs={'placeholder':'Describe your idea'}),
		}
	def save(self, commit=True):
		project=super().save(commit=False)
		if commit:
			project.save()
		return project
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)		

class ReportForm(forms.ModelForm):
	class Meta:
		model = Report
		fields =['file']

class AssignReviewerForm(forms.ModelForm):
	class Meta:
		model=Project
		fields =('reviewee',)
		'''
	def __init__(self):
		#super(AssignReviewerForm, self).__init__(self)
		self.fields['reviewee'].queryset = User.objects.all().filter(is_reviewer=True)
		'''