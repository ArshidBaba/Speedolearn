from django.shortcuts import render
from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)

from .serializers import (
    VendorListSerializer,
    TrainingListSerializer,
    CourseListSerializer,
    TopicListSerializer,
    CourseDetailSerializer,
    ProductFAQListSerializer,
    TestimonialSerializer,
)

from superadmin.models import Course, Training, Topic, Vendor, ProductFAQ, Testimonial

from .filters import CourseFilter

from .models import Enquiry, Enrollment, Instructor, ContactUs, EmailSubscriber


@api_view(["GET"])
def vendorList(request):
    try:
        page_size = request.query_params["limit"]
    except:
        page_size = 10

    vendor = Vendor.objects.all()
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    result_page = paginator.paginate_queryset(vendor, request)
    serializer = VendorListSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)


############################# Training Section   ############################


@api_view(["GET"])
def trainingList(request):
    try:
        page_size = request.query_params["limit"]
    except:
        page_size = 10
    training = Training.objects.all()
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    result_page = paginator.paginate_queryset(training, request)
    serializer = TrainingListSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
def trainingDetails(request, pk):
    try:
        page_size = request.query_params["limit"]
    except:
        page_size = 10
    course = Course.objects.filter(training=pk)
    print(course)
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    result_page = paginator.paginate_queryset(course, request)
    serializer = CourseListSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)


#############################   Course Section   ############################


@api_view(["GET"])
def courseList(request):
    try:
        page_size = request.query_params["limit"]
    except:
        page_size = 10
    courses = Course.objects.all().order_by("start_date")
    trainings = request.GET.getlist("trainings[]")
    vendors = request.GET.getlist("vendors[]")
    print(request.GET)
    if trainings or vendors:
        if trainings or vendors:
            query = Q()
            if trainings:
                query |= Q(training__id__in=trainings)
            if vendors:
                query |= Q(training__vendor__id__in=vendors)
            courses = Course.objects.filter(query).order_by("start_date")

        paginator = PageNumberPagination()
        paginator.page_size = page_size
        courses = paginator.paginate_queryset(courses, request)

        serializer = CourseListSerializer(courses, many=True)
        return paginator.get_paginated_response(serializer.data)
    else:
        course = Course.objects.all().order_by("start_date")
        filterset = CourseFilter(request.GET, queryset=course)
        if filterset.is_valid():
            course = filterset.qs
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            courses = paginator.paginate_queryset(course, request)
            serializer = CourseListSerializer(courses, many=True)

            return paginator.get_paginated_response(serializer.data)


#############################   Topic Section   ############################


@api_view(["GET"])
def courseDetail(request, pk):
    """
    Course Detail Endpoint
    """
    try:
        course = Course.objects.get(pk=pk)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Invalid Course ID",
            "data": [],
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    serializer = CourseDetailSerializer(
        course, many=False, context={"request": request}
    )
    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "Course Details Fetched Successfully",
        "data": serializer.data,
    }
    return Response(response, status=status.HTTP_200_OK)


#############################   Course Enquiry Section   ############################


@api_view(["POST"])
def makeEquiry(request):
    data = request.data
    try:
        course = Course.objects.get(pk=data["course"])
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Invalid Course ID",
            "data": [],
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)

    enquiry = Enquiry.objects.create(phone=data["phone"], course=course)
    response = {
        "status": "Success",
        "code": status.HTTP_201_CREATED,
        "message": "Equiry Created Successfully",
        "data": [],
    }

    return Response(response, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def enroll(request):
    data = request.data
    try:
        course = Course.objects.get(pk=data["course_id"])
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Invalid Course ID",
            "data": [],
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)

    enrollment = Enrollment.objects.create(
        course=course, name=data["name"], email=data["email"], phone=data["phone"]
    )

    response = {
        "status": "Success",
        "code": status.HTTP_201_CREATED,
        "message": "Enrollment Successful",
        "data": [],
    }

    return Response(response, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def enrollInstructor(request):
    data = request.data
    instructor = Instructor.objects.create(
        name=data["name"], email=data["email"], phone=data["phone"]
    )
    response = {
        "status": "Success",
        "code": status.HTTP_201_CREATED,
        "message": "Enrollment Successful",
        "data": [],
    }

    return Response(response, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def listFAQs(request):
    faqs = ProductFAQ.objects.all()
    serializer = ProductFAQListSerializer(faqs, many=True)

    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "FAQs fetched Successfully",
        "data": serializer.data,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])
def listTestimonials(request):
    testimonials = Testimonial.objects.all()
    serializer = TestimonialSerializer(testimonials, many=True)

    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "Testimonials fetched Successfully",
        "data": serializer.data,
    }

    return Response(response, status=status.HTTP_200_OK)


@api_view(["POST"])
def contactUs(request):
    data = request.data

    contact = ContactUs.objects.create(
        full_name=data["full_name"],
        email=data["email"],
        phone=data["phone"],
        message=data["message"],
    )

    response = {
        "status": "Success",
        "code": status.HTTP_201_CREATED,
        "message": "Message Sent Successfully",
        "data": [],
    }

    return Response(response, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def subscribe(request):
    data = request.data
    subscriber = EmailSubscriber.objects.create(email=data["email"])

    response = {
        "status": "Success",
        "code": status.HTTP_201_CREATED,
        "message": "Subscribed Successfully",
        "data": [],
    }
    return Response(response, status=status.HTTP_201_CREATED)
