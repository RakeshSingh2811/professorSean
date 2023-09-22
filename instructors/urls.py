from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path("", views.index.as_view(), name="instructorHome"),
    path("courses/", views.Course_Page.as_view(), name="courseList"),
    path("chapter/<id>", views.Chapter_Page.as_view(), name="chaptersList"),
    path("topic/<id>", views.Topic_Page.as_view(), name="topicList"),
    path("topicDetail/<id>", views.Topic_Details.as_view(), name="topicDetails"),
    path("topicUpdate/<pk>", views.TopicUpdateView.as_view(), name="topicUpdate"),
    path("topicCreate", views.TopicCreateView.as_view(), name="topicCreate"),
    path("topicDelete/<pk>", views.TopicDeleteView.as_view(), name="topicDelete"),
    path("courseCreate", views.CourseCreateView.as_view(), name="courseCreate"),
    path("courseDelete/<pk>", views.CourseDeleteView.as_view(), name="courseDelete"),
    path("courseUpdate/<pk>", views.CourseUpdateView.as_view(), name="courseUpdate"),
    path("chapterCreate", views.ChapterCreateView.as_view(), name="chapterCreate"),
    path("chapterDelete/<pk>", views.ChapterDeleteView.as_view(),
         name="chapterDelete"),
    path("chapterUpdate/<pk>", views.ChapterUpdateView.as_view(),
         name="chapterUpdate"),
]
