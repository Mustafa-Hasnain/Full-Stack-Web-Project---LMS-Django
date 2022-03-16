from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'), #Index page
    path('lsign/', views.LearnerSignUpView.as_view(), name = 'lsign'), #Register
    path('login_form/', views.login_form, name = 'login_form'), #login
    path('login/', views.loginView, name = 'login'), #login return function
    ##Admin Views
    path('logout/', views.logoutView, name = 'logout'), #admin logout
    path('dashboard/', views.dashboard, name = 'dashboard'), #admin dashboard
    path('isign/', views.InstructorSignupView.as_view(), name='isign'), #admin add instructor
    path('addlearner/', views.AdminLearner.as_view(), name='addlearner'), #admin add learner
    path('course/', views.course, name = 'course'), #admin add course
    path('adminpost/', views.AdminCreatePost.as_view(), name = 'apost'), #Admin post Announcements 
    path('adminpostlist/', views.AdminListPost, name = 'alstpost'), #List Announcements Post
    path('adminUsrlist/', views.AdminManageUser, name = 'aUsrlst'), #List Users
    path('UsrDel/<int:id>', views.deleteUser, name = 'delUsr'), #Delete User
    path('createAdmin/', views.registerAdmin, name= 'createAdmin'), #create admin form
    path('regAdmin/', views.create_admin, name='RegAdmin'),#Create Admin page
    #Instructor Views
    path('Instructor/', views.home_instructor, name='Instructor'), #Instructor Dashboard
    path('quiz_create/', views.QuizCreateView.as_view(), name='createQuiz'), #Instructor Create Quiz
    path('inspost/', views.InstuctorCreatePost.as_view(), name = 'inspost'), #Admin post Announcements 
    path('inspostlist/', views.InstructorListPost, name = 'inslstpost'), #List Announcements Post
    path('insUsrlist/', views.InstructorManageUser, name = 'InsUsrlst'), #List Users
    path('tutorial/', views.tutorial, name = 'tutorial'),#Instructor Add Tutorial
    path('pubtutorial/', views.publish_tutorial, name = 'tutorialpost'),#Instructor POST Tutorial
    path('lsttutorial/', views.itutorial, name = 'list_tutorial'), #Instructor list Tutorial
    #Learner Views
    path('learner/', views.home_Learner, name = 'learner'),
    path('ltutorial', views.list_tutorial, name = 'ltutorial'), 
    path('lpost/', views.LearnerListPost, name = 'lpost'),
    path('interests/', views.LearnerInterestsView.as_view(), name='interests'),

    ]