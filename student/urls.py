from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', auth_views.LoginView.as_view(
        template_name="student/login.html"), name="studentlogin"),
    path('login/', auth_views.LoginView.as_view(template_name="student/login.html"),
         name="studentlogin"),
    path('logout/', auth_views.LogoutView.as_view(), name="studentlogout"),
    path('signup/', views.Signup.as_view(), name="studentsignup"),
    path("course/", views.Courses.as_view(), name="studentcourse"),
    path("courseDetails/<course_id>",
         views.CourseDetails.as_view(), name="courseDetails"),
    path("topicDetails/<course_id>/chapter/<chapter_id>/topic/<topic_id>",
         views.TopicDetails.as_view(), name="topicDetails")
]
