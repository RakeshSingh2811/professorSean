from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', auth_views.LoginView.as_view(
        template_name="student/login.html"), name="login"),
    path('login/', auth_views.LoginView.as_view(template_name="student/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('signup/', views.Signup.as_view(), name="signup"),
    path("course/", views.Courses.as_view(), name="course"),
    path("courseDetails/<course_id>",
         views.CourseDetails.as_view(), name="courseDetails"),
    path("topicDetails/<course_id>/chapter/<chapter_id>/topic/<topic_id>",
         views.TopicDetails.as_view(), name="topicDetails")
]
