from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from classroom.models import (Solution, Idea, Student, StudentSolution,
                              Subject, User)


class TeacherSignUpForm(UserCreationForm):
    first_name =  forms.CharField( max_length=100, required=True)
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user

class ReviewerSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length= 254, required=True)
    first_name= forms.CharField(max_length=50, required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_reviewer = True
        if commit:
            user.save()
        return user

class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length= 254, required=True)
    first_name= forms.CharField(max_length=50, required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]
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

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('text', )


class TakenProjectForm(forms.ModelForm):
    solution = forms.ModelChoiceField(
        queryset=Solution.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentSolution
        fields = ('solution', )

    def __init__(self, *args, **kwargs):
        Idea = kwargs.pop('Idea')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = Idea.answers.order_by('text')