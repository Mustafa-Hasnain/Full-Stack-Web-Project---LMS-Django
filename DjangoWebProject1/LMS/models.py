from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import escape, mark_safe
from django.contrib.auth import get_user_model
from embed_video.fields import EmbedVideoField
# Create your models here.

class User(AbstractUser):
    is_learner = models.BooleanField(default = False)
    is_instructor = models.BooleanField(default = False)
    is_admin = models.BooleanField(default = False)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    avatar = models.ImageField(upload_to = '', default = 'no-imag.jpg', blank = True)
    first_name = models.CharField(max_length = 50, default = '')
    last_name = models.CharField(max_length = 50, default = '')
    email = models.EmailField(default = 'non@gmail.com')
    birth_date = models.DateField()
    city = models.CharField(max_length = 100, default = 'Karachi')
    country = models.CharField(max_length = 100, default = 'Pakistan')

    def __str__(self):
        return self.user.username

class Announcements(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    posted_at = models.DateTimeField(auto_now = True, null = True)

    def __str__(self):
        return str(self.content)

class Course(models.Model):
    name= models.CharField(max_length = 50)
    code = models.CharField(max_length = 7, default = 'CS-###')

    def __str__(self):
        return self.name

class Tutorial(models.Model):
    title = models.CharField(max_length = 50)
    content = models.TextField()
    thumb = models.ImageField(upload_to = '', null = True, blank = True)
    course = models.ForeignKey(Course, on_delete = models.CASCADE, default = '')
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    video = EmbedVideoField(blank = True, null=True)
    

class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'quizzes')
    name = models.CharField(max_length = 50)
    course = models.ForeignKey(Course, on_delete = models.CASCADE, default = 'quizzes')

    def __str__(self):
        return self.name

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=255)

    def __str__(self):
        return self.text

class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    interests = models.ManyToManyField(Course, related_name='interested_learners')

    def __str__(self):
        return self.user.username

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interest = models.ManyToManyField(Course, related_name="more_locations")

class TakenQuiz(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)






