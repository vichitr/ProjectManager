from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from classroom.models import (Solution, Idea, Student, StudentSolution,
                              Subject, User)


class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user

class ReviewerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_reviewer = True
        if commit:
            user.save()
        return user

class StudentSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        #student = Student.objects.create(user=user)
        #student.courses.add(*self.cleaned_data.get('courses'))
        return user


class StudentCoursesForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('courses', )
        widgets = {
            'courses': forms.CheckboxSelectMultiple
        }


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