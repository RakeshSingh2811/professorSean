from django.shortcuts import render
from django.views import generic
from course.models import Chapter, Course, Topic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms

# Create your views here.


class Signup(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'student/signup.html'


class Courses(LoginRequiredMixin, generic.TemplateView):
    template_name = "student/courses.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Courses, self).get_context_data(*args, **kwargs)
        context['courses'] = Course.objects.all()
        return context


class CourseDetails(LoginRequiredMixin, generic.TemplateView):
    template_name = "student/courseDetails.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CourseDetails, self).get_context_data(*args, **kwargs)
        course_id = context['course_id']
        course = Course.objects.get(id=course_id)
        context['course'] = course
        chapters = Chapter.objects.filter(course=course)
        context['chapters'] = chapters
        context['current_chapter'] = chapters.first()
        topicList = []
        currentTopic = ''
        for chapter in chapters:
            topics = Topic.objects.filter(chapter=chapter)
            for topic in topics:
                if (currentTopic == ''):
                    currentTopic = topic
                topicList.append(topic)
        context["topics"] = topicList
        context['current_topic'] = currentTopic
        return context


class TopicDetails(LoginRequiredMixin, generic.TemplateView):
    template_name = "student/courseDetails.html"

    def get_context_data(self, *args, **kwargs):
        context = super(TopicDetails, self).get_context_data(*args, **kwargs)
        course = Course.objects.get(id=context['course_id'])
        print(context)
        context['course'] = course
        chapters = Chapter.objects.filter(course=course)
        context['chapters'] = chapters
        context['current_chapter'] = Chapter.objects.get(
            id=context['chapter_id'])
        topicList = []
        for chapter in chapters:
            topics = Topic.objects.filter(chapter=chapter)
            for topic in topics:
                topicList.append(topic)
        context["topics"] = topicList
        context["current_topic"] = Topic.objects.get(id=context['topic_id'])
        return context
