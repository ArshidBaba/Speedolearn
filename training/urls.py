from django.urls import path, include
from . import views

urlpatterns = [
    path("vendor-list/", views.vendorList, name="vendor-list"),
    path("training-list/", views.trainingList, name="training-list"),
    path("training-details/<int:pk>/", views.trainingDetails, name="training-details"),
    path("course-list/", views.courseList, name="course-list"),
    path("course-detail/<int:pk>/", views.courseDetail, name="topic-list"),
    path("create-equiry/", views.makeEquiry, name="make-equiry"),
    path("enroll/", views.enroll, name="enroll"),
    path("instructor/", views.enrollInstructor, name="enroll-instructor"),
    path("faqs/", views.listFAQs, name="list-faqs"),
    path("testimonials/", views.listTestimonials, name="create-testimonial"),
    path("contact-us/", views.contactUs, name="contact-us"),
    path("subscribe/", views.subscribe, name="subscribe"),
]
