from django.shortcuts import render
from django.urls import reverse_lazy
from course import models
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView


class index(TemplateView):
    template_name = "instructors/home.html"


class Course_Page(TemplateView):
    template_name = "instructors/courses.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Course_Page, self).get_context_data(*args, **kwargs)
        context['courses'] = models.Course.objects.all()
        return context


class Chapter_Page(TemplateView):
    template_name = "instructors/chapters.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Chapter_Page, self).get_context_data(*args, **kwargs)
        id = context['id']
        context['chapters'] = models.Chapter.objects.filter(course=id)
        return context


class Topic_Page(TemplateView):
    template_name = "instructors/topics.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Topic_Page, self).get_context_data(*args, **kwargs)
        id = context['id']
        context['topics'] = models.Topic.objects.filter(chapter=id)
        return context


class Topic_Details(TemplateView):
    template_name = "instructors/topicDetails.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Topic_Details, self).get_context_data(*args, **kwargs)
        id = context['id']
        context['topic'] = models.Topic.objects.get(id=id)
        return context


class TopicUpdateView(UpdateView):
    model = models.Topic
    fields = '__all__'
    template_name = "instructors/topic_Update.html"

    def get_success_url(self) -> str:
        return reverse_lazy('topicDetails', kwargs={'id': self.object.pk})


class TopicCreateView(CreateView):
    model = models.Topic
    fields = '__all__'
    template_name = "instructors/topic_Update.html"

    def get_success_url(self) -> str:
        return reverse_lazy('topicDetails', kwargs={'id': self.object.pk})


class TopicDeleteView(DeleteView):
    model = models.Topic
    template_name = "instructors/topic_Update.html"

    def get_success_url(self) -> str:
        return reverse_lazy('topicList', kwargs={'id': self.object.chapter.id})


class CourseCreateView(CreateView):
    model = models.Course
    fields = "__all__"
    template_name = "instructors/courseForm.html"
    success_url = "/instructors/courses"


class CourseUpdateView(UpdateView):
    model = models.Course
    fields = "__all__"
    template_name = "instructors/courseForm.html"
    success_url = "/instructors/courses"


class CourseDeleteView(DeleteView):
    model = models.Course
    template_name = "instructors/courseForm.html"
    success_url = "/instructors/courses"


class ChapterCreateView(CreateView):
    model = models.Chapter
    fields = "__all__"
    template_name = "instructors/chapterForm.html"

    def get_success_url(self) -> str:
        return reverse_lazy('chaptersList', kwargs={'id': self.object.course.id})


class ChapterUpdateView(UpdateView):
    model = models.Chapter
    fields = "__all__"
    template_name = "instructors/chapterForm.html"

    def get_success_url(self) -> str:
        return reverse_lazy('chaptersList', kwargs={'id': self.object.course.id})


class ChapterDeleteView(DeleteView):
    model = models.Chapter
    template_name = "instructors/chapterForm.html"

    def get_success_url(self) -> str:
        return reverse_lazy('chaptersList', kwargs={'id': self.object.course.id})
