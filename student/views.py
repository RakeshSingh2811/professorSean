from django.shortcuts import render
from django.views.generic import *
from course.models import Chapter, Course, Topic
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
import stripe
from django.shortcuts import *
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json

# Create your views here.


class Signup(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'student/signup.html'


class Courses(LoginRequiredMixin, TemplateView):
    template_name = "student/courses.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Courses, self).get_context_data(*args, **kwargs)
        context['courses'] = Course.objects.all()
        return context


class CourseDetails(LoginRequiredMixin, TemplateView):
    template_name = "student/courseDetails.html"

    def get(self, *args, **kwargs):
        course = Course.objects.get(id=kwargs.get('course_id'))
        user = self.request.user
        order = Order.objects.filter(
            email=user.email, course=course, has_paid=True)
        if (len(order) == 0):
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


class TopicDetails(LoginRequiredMixin, TemplateView):
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
    data = json.loads(request.body)
    course = Course.objects.get(id=data['id'], name=data['course'])
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    session = stripe.checkout.Session.create(
        customer_email=request.user.email,
        client_reference_id=request.user.id if request.user.is_authenticated else None,
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': course,
                },
                'unit_amount': int(course.price*100),

            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('payment_success'))+"?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('payment_cancel'))
    )
    order = Order()
    order.email = request.user.email
    order.course = course
    order.stripe_payment_intent = session['id']
    order.amount = int(course.price*100)
    order.save()
    return JsonResponse({'id': session.id})


def payment(request, course_id):
    course = Course.objects.get(id=course_id)
    chapters = Chapter.objects.filter(course=course)
    topics = []
    stripe_publishable_key = settings.STRIPE_PUBLIC_KEY
    for chapter in chapters:
        topic = Topic.objects.filter(chapter=chapter)
        for t in topic:
            topics.append(t)
    return render(request, 'student/checkout.html', {"course": course, "chapters": chapters, "topics": topics, 'stripe_publishable_key': stripe_publishable_key})


# success view

class PaymentSuccessView(TemplateView):
    template_name = 'student/success.html'

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        stripe.api_key = settings.STRIPE_PRIVATE_KEY
        session = stripe.checkout.Session.retrieve(session_id)
        order = get_object_or_404(
            Order, stripe_payment_intent=session_id)
        order.has_paid = True
        order.save()
        return render(request, self.template_name)


# cancel view


def cancel(request):
    return render(request, 'student/cancel.html')
