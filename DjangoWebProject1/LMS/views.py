from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views import generic
#from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.generic.edit import CreateView, UpdateView, DeleteView #Packages for Create Update and DeleteView
from django.http import HttpResponse, Http404
#from .models import Customer, Profile
from .form import LearnerSignUpForm, InstructorSignUpForm, QuestionForm, LearnerInterestsForm, LearnerCourse, UserForm, ProfileForm, PostForm
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.conf import settings
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, date
from django.core.exceptions import ValidationError
from . import models
from django.db.models import Avg, Count, Sum
#from django.form import inlineformset_factory
from .models import Profile, Quiz, Learner, User, Course, Tutorial, Announcements
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,PasswordChangeForm)
from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalFormView,
    BSModalCreateView,   ###These bootstrap imports are all recomendation of bootstrap##
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)

def home(request):
    return render(request, 'Home.html')

def login_form(request):
    return render(request, 'login.html')


###LearnerViews###

#Register as a Learner
class LearnerSignUpView(CreateView): #Here we a using module Create View and it requires some param from form.py
    model = User
    form_class = LearnerSignUpForm #This is made in form.py
    template_name = 'signup_form.html' #This requires a template name as well

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'learner' #Here we are making Register as a User
        return super().get_context_data(**kwargs)

    def form_valid(self, form): #Form validation #Type of Default Function For validation
        user = form.save()
        login(self.request, user) #After Successful Validation we want the user to be logged in
        #return('home') #Redirect to Home page
        return redirect('home') #for redirecting the student to Std dashboard

#login
def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password = password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('dashboard')
            elif user.is_instructor:
                return redirect('Instructor')
            elif user.is_learner:
                return redirect('learner')
            else:
                return redirect('login_form')
        else:
            messages.info(request, "Invalid Username or Password")
            return redirect('login_form')

#Logout
def logoutView(request):
    logout(request)
    return redirect('home')

###Admin Views#### 
def dashboard(request):
    learner = User.objects.filter(is_learner=True).count() #Counting###
    instructor = User.objects.filter(is_instructor=True).count()
    course = Course.objects.all().count()
    users = User.objects.all().count
    context = {'learner':learner, 'instructor':instructor,'course':course, 'users':users}

    return render(request, 'LMS/admin/home.html', context)
   

def create_admin(request):
    return render(request, 'LMS/admin/create_user.html')

#Admin Adding Learner
class AdminLearner(CreateView): #Here we a using module Create View and it requires some param from form.py
    model = User
    form_class = LearnerSignUpForm #This is made in form.py
    template_name = 'LMS/admin/learner_signup_form.html' #This requires a template name as well

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'learner' #Here we are making Register as a User
        return super().get_context_data(**kwargs)

    def form_valid(self, form): #Form validation #Type of Default Function For validation
        user = form.save()
        #login(self.request, user) #After Successful Validation we want the user to be logged in
        messages.success(self.request, "Learner was added succesfully!!")
        #return('home') #Redirect to Home page
        return redirect('addlearner') #for redirecting the student to Std dashboard

#Instructor Registration in Admin 
class InstructorSignupView(CreateView): #Here we a using module Create View and it requires some param from form.py
    model = User
    form_class = InstructorSignUpForm #This is made in form.py
    template_name = 'LMS/admin/signup_form.html' #This requires a template name as well

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'instructor' #Here we are making Register as a User
        return super().get_context_data(**kwargs)

    def form_valid(self, form): #Form validation #Type of Default Function For validation
        user = form.save() #Here we are adding it not logging it...
        messages.success(self.request, "Instructor was added succesfully!!")
        #return('home') #Redirect to Home page
        return redirect('isign') #for redirecting the student to Std dashboard

#def Register Course
def course(request):
    if request.method == 'POST':
        name = request.POST['name']
        color = request.POST['code']
        a = Course(name=name, code=color)
        a.save()
        messages.success(request, 'New Course Was Registed Successfully')
        return redirect('course')
    else:
        return render(request, 'LMS/admin/course.html')	

#Admin Announcement Create post
class AdminCreatePost(CreateView):
    model = Announcements
    form_class = PostForm
    template_name = 'LMS/admin/post_form.html'
    #success_url = reverse_lazy('dashboard') #After successful post


    def form_valid(self, form): #Type of Default Function For validation
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        messages.success(self.request, 'Announcement was Posted Succesfully')
        return redirect('alstpost') 

#Admin Lists Posts
def AdminListPost(request):
    admin_list = Announcements.objects.filter(posted_at__lt = timezone.now()).order_by('-posted_at')
    return render(request, 'LMS/admin/list_post.html', {'admin_list':admin_list})

#Admin Manage User
def AdminManageUser(request):
    if request.method == 'GET':
        usr_list = User.objects.all().order_by('id')
        return render(request, 'LMS/admin/list_user.html', {'usr_list':usr_list})
    else:
        usr_list = User.objects.filter(username__startswith = request.POST['text'])
        return render(request, 'LMS/admin/list_user.html', {'usr_list':usr_list})

    

#Admin Delete User
def deleteUser(request, id):
    usr = User.objects.get(pk=id)
    usr.delete()
    return redirect('aUsrlst')

#Admin RegisterAdmin
def registerAdmin(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password = make_password(password)


        a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_admin=True)
        a.save()
        messages.success(request, 'Admin Was Created Successfully')
        return redirect('aUsrlst')
                         ##So here we Are Rendering path so to use the .html file we will create above function
                         ##That will return only the html file
    else:
        messages.error(request, 'Admin Was Not Created Successfully')
        return render(request, 'LMS/admin/create_user.html')
    

#Instructor Views
def home_instructor(request):
    learner = User.objects.filter(is_learner=True).count() #Counting###
    instructor = User.objects.filter(is_instructor=True).count()
    course = Course.objects.all().count()
    users = User.objects.all().count
    context = {'learner':learner, 'instructor':instructor,'course':course, 'users':users}
    return render(request, 'LMS/instructor/home.html', context)

#Instructor CreateQuiz (Title only not Questions)
class QuizCreateView(CreateView): #Here we are using CreateView Module so we are creating class
    model = Quiz
    fields = ('name', 'course')
    template_name = 'LMS/instructor/quiz_add_form.html'

    def form_valid(self, form): #This module helps in validating form as well
        quiz = form.save(commit=False)
        quiz.owner = self.request.user #user is a default attribute 
        quiz.save()
        messages.success(self.request, "Quiz Created!!")
        return redirect('Instructor')



#Instructor Announcements POST
class InstuctorCreatePost(CreateView):
    model = Announcements
    form_class = PostForm
    template_name = 'LMS/instructor/post_form.html'
    #success_url = reverse_lazy('dashboard') #After successful post


    def form_valid(self, form): #Type of Default Function For validation
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        messages.success(self.request, 'Announcement was Posted Succesfully')
        return redirect('inslstpost') 

#Insructor Lists Posts
def InstructorListPost(request):
    admin_list = Announcements.objects.filter(posted_at__lt = timezone.now()).order_by('posted_at')
    return render(request, 'LMS/instructor/list_post.html', {'admin_list':admin_list})

#Instructor Manage User
def InstructorManageUser(request):
    if request.method == 'GET':
        usr_list = User.objects.all().order_by('id')
        return render(request, 'LMS/instructor/list_user.html', {'usr_list':usr_list})
    else:
        usr_list = User.objects.filter(username__startswith = request.POST['text'])
        return render(request, 'LMS/instructor/list_user.html', {'usr_list':usr_list})

#Instructor Add Tutorial
def tutorial(request):
    courses = Course.objects.only('id', 'name')
    context = {'courses':courses}
    return render(request, 'LMS/instructor/tutorial.html',context)

#Instructor Manage Tutorial
def publish_tutorial(request):
    if request.method == 'POST':
        title = request.POST['title']
        course_id = request.POST['course_id']
        content = request.POST['content']
        thumb = request.FILES['thumb']
        current_user = request.user
        author_id = current_user.id
        print(author_id)
        print(course_id)
        a = Tutorial(title=title, content=content, thumb=thumb, user_id=author_id, course_id=course_id)
        a.save()
        messages.success(request, 'Tutorial was published successfully!')
        return redirect('tutorial')
    else:
        messages.error(request, 'Tutorial was not published successfully!')
        return redirect('tutorial')


#Instructor List Tutorial
def itutorial(request):
   tutorials = Tutorial.objects.all().order_by('-id')
   tutorials = {'tutorials':tutorials}
   return render(request, 'LMS/instructor/list_tutorial.html', tutorials)


###LearnerViews####

#Learner home Page
def home_Learner(request):
    learner = User.objects.filter(is_learner=True).count() #Counting###
    instructor = User.objects.filter(is_instructor=True).count()
    course = Course.objects.all().count()
    users = User.objects.all().count()
    context = {'learner':learner, 'instructor':instructor,'course':course, 'users':users}
    return render(request, 'LMS/learner/home.html', context)

#Learner List of Tutorials
def list_tutorial(request):
   tutorials = Tutorial.objects.all().order_by('-id')
   tutorials = {'tutorials':tutorials}
   return render(request, 'LMS/learner/list_tutorial.html', tutorials)

#Learner view Announcements
def LearnerListPost(request):
    admin_list = Announcements.objects.filter(posted_at__lt = timezone.now()).order_by('posted_at')
    return render(request, 'LMS/learner/list_post.html', {'admin_list':admin_list})

#Learner Update Courses
class LearnerInterestsView(UpdateView): #HUsing UpdateView module for updating the form that is taken from form.py
    model = Learner
    form_class = LearnerInterestsForm
    template_name = 'LMS/learner/interest_from.html'
    success_url = reverse_lazy('interests')

    def get_object(self):
        return self.request.user.learner

    def form_valid(self, form):
        messages.success(self.request, 'Course Was Updated Successfully')
        return super().form_valid(form)
