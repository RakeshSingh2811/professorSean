from django.shortcuts import render
from django.views import generic
from course.models import Chapter, Course, Topic
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
import stripe
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'http://127.0.0.1:8000'


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

    def get(self, *args, **kwargs):
        course = Course.objects.get(id=kwargs.get('course_id'))
        user = self.request.user
        subscription = Subsription.objects.filter(student=user, course=course)
        if (len(subscription) == 0):
            return redirect('payment', course_id=course.id)
        return super(CourseDetails, self).get(*args, **kwargs)

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
# home view


@csrf_exempt
def create_checkout_session(request):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': 'Intro to Django Course',
                },
                'unit_amount': 10000,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment_success')),
        cancel_url=request.build_absolute_uri(reverse('payment_cancel'))
    )
    return JsonResponse({'id': session.id})


def payment(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'student/checkout.html', {course: course})

# success view


def success(request):
    return render(request, 'student/success.html')

    # cancel view


def cancel(request):
    return render(request, 'student/cancel.html')
