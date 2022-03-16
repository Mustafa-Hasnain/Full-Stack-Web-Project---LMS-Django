from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction 
from django.forms.utils import ValidationError

from LMS.models import User, Announcements, Course, Question,Learner

#POST Announcement Form
class PostForm(forms.ModelForm):
    class Meta:
        model = Announcements
        fields = ('content', )

#Profile Form
class ProfileForm(forms.ModelForm):
    email=forms.EmailField(widget=forms.EmailInput())
    confirm_email=forms.EmailField(widget=forms.EmailInput())

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            ]
        #Confirming Emails
    def confirm(self):
        cleaned_data = super(ProfileForm, self).clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")

        if email != confirm_email:
            raise forms.ValidationError("Emails Must Match! PLZ TRY AGAIN")

        ##USER FORMS
class UserForm(forms.ModelForm):
     class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

        ##INSRTUCTOR FORM
class InstructorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
    
    def __init__(self, *args, **kwargs):
        super(InstructorSignUpForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_instructor = True
        if commit:
            user.save()
        return user

    #Creating a Form for Learner
class LearnerSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(queryset=Course.objects.all(),widget=forms.CheckboxSelectMultiple,
                                                required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
            super(LearnerSignUpForm, self).__init__(*args, **kwargs)
            for fieldname in ['username', 'password1', 'password2']:
                self.fields[fieldname].help_text = None    

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_learner = True
        user.save()
        learner = Learner.objects.create(user=user)
        learner.interests.add(*self.cleaned_data.get('interests'))
        return user

    
    ##LEARNER FORM (Interstes)

class LearnerInterestsForm(forms.ModelForm):
    class Meta:
        model = Learner
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }


        #LEARNER FORM(QUESTION)
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', )


        #FOR LEARNER COURSES
class LearnerCourse(forms.ModelForm):
    class Meta:
        model = Learner
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }

    @transaction.atomic
    def save(self):
        learner = Learner()
        learner.interests.add(*self.cleaned_data.get('interests'))
        return learner_id












