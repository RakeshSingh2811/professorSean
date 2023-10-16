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
from django.contrib import messages
import json
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
        order = Order.objects.filter(email=user.email, course=course)
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
    data = json.loads(request.body.decode("utf-8"))
    course = Course.objects.get(id=data['id'], name=data['course'])
    order = Order(email=" ", paid="False", amount=0,
                  description=" ", course=course)
    order.save()
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
        metadata={
            "order_id": order.id
        },
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('studentcourse')),
        cancel_url=request.build_absolute_uri(reverse('payment_cancel'))
    )
    messages.success(
        request, "Payment Successfully done! You can access the course now")
    return JsonResponse({'id': session.id})


def payment(request, course_id):
    course = Course.objects.get(id=course_id)
    chapters = Chapter.objects.filter(course=course)
    topics = []
    for chapter in chapters:
        topic = Topic.objects.filter(chapter=chapter)
        for t in topic:
            topics.append(t)
    return render(request, 'student/checkout.html', {"course": course, "chapters": chapters, "topics": topics})

# success view


def success(request):
    return render(request, 'student/success.html')

    # cancel view


def cancel(request):
    return render(request, 'student/cancel.html')


@csrf_exempt
def stripe_webhook(request):
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
        # Handle the checkout.session.completed event
     # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # NEW CODE
        session = event['data']['object']
        # getting information of order from session
        customer_email = session["customer_details"]["email"]
        price = session["amount_total"] / 100
        sessionID = session["id"]
        # grabbing id of the order created
        ID = session["metadata"]["order_id"]
        # Updating order
        Order.objects.filter(id=ID).update(
            email=customer_email, amount=price, paid=True, description=sessionID)

    return HttpResponse(status=200)
