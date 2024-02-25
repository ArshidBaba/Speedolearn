from django.utils import timezone
import json
from django.db import models
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from accounts.serializers import UserSerializerWithToken
from accounts.models import CustomUser

from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
    parser_classes,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from training.models import Enquiry, Enrollment, Instructor, ContactUs, EmailSubscriber
from accounts.models import CustomUser


from .models import (
    Vendor,
    Training,
    Course,
    Topic,
    Feature,
    ResultsAndJobOpportunities,
    ExamAndCertification,
    JobImage,
    FAQ,
    ProductFAQ,
    Testimonial,
    Prerequisite,
)
from .filters import (
    CourseFilter,
    CourseSearchFilter,
    ProductFAQSearchFilter,
    ProductFAQFilter,
    EmailSubscriberSearchFilter,
    ContactQueryFilter,
    ContactQuerySearchFilter,
    InstructorEnquiriesSearchFilter,
    InstructorEnquiriesFilter,
    TrainingFilter,
    TrainingSearchFilter,
    EnrollmentFilter,
    EnrollmentSearchFilter,
    EnquiriesSearchFilter,
    EnquiriesFilter,
    VendorSearchFilter,
)
from .permissions import IsSuperUser
from .serializers import (
    CourseCreationSerializer,
    TrainingSerializer,
    TopicCreationSerializer,
    EnrollmentSerializer,
    InstructorSerializer,
    EnquiryListSerializer,
    CourseListSerializer,
    TrainingListSerializer,
    VendorListSerializer,
    ProductFAQListSerializer,
    TestimonialSerializer,
    ContactQueriesSerializer,
    ContactQuerySerializer,
    EmailSubscriberSerializer,
    EnquiryEditSerializer,
    VendorEditSerializer,
    ChangePasswordSerializer,
    PersonalDetailsSerializer,
    ContactDetailsSerializer,
    FAQSerializer,
)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer for custom token claims."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["email"] = user.email
        token["is_superuser"] = user.is_superuser

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            print(k, v)
            data[k] = v
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    """Custom Token Pair View."""

    serializer_class = MyTokenObtainPairSerializer


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def createVendor(request):
    """Endpoint to create new Vendor."""
    data = request.data
    try:
        vendor = Vendor.objects.create(
            vendored=data["vendored"],
            name=data["name"],
            logo=request.FILES.get("logo"),
            # created_at=data["created_at"],
            is_live_on_website=data["is_live_on_website"],
        )
        print(vendor)
        response = {
            "status": "Success",
            "code": status.HTTP_201_CREATED,
            "message": "Vendor created successfully",
            "data": [],
        }
        return Response(response, status=status.HTTP_201_CREATED)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid Payload",
            "data": [],
        }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def editVendor(request, pk):
    """Edit Vendor endpoint."""
    data = request.data

    try:
        vendor = Vendor.objects.get(pk=pk)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Invalid Vendor ID",
            "data": [],
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    serializer = VendorEditSerializer(vendor, data=data, many=False, partial=True)
    if serializer.is_valid():
        serializer.save()

        response = {
            "status": "Success",
            "code": status.HTTP_200_OK,
            "message": "Vendor Edited Successfully",
            "data": [],
        }

        return Response(response, status=status.HTTP_200_OK)
    else:
        response = {
            "status": "Failure",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "InvalidPayload",
            "data": [],
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def deleteVendor(request, pk):
    """Delete Vendor endpoint."""
    try:
        vendor = Vendor.objects.get(pk=pk)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Invalid Vendor ID",
            "data": [],
        }

        return Response(response, status=status.HTTP_404_NOT_FOUND)
    vendor.delete()
    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "Vendor Deleted Successfully!",
        "data": [],
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def createTraining(request):
    """Endpoint to create a new Training."""
    data = request.data
    vendor = Vendor.objects.get(pk=data["vendor"])
    training = Training.objects.create(
        vendor=vendor,
        name=data["name"],
        image=request.FILES.get("image"),
        live_on_website=data["live_on_website"],
        created_at=data["created_at"],
    )

    response = {
        "status": "Success",
        "code": status.HTTP_201_CREATED,
        "message": "Training created successfully",
        "data": [],
    }

    return Response(response, status=status.HTTP_200_OK)


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
@transaction.atomic
def createCourse(request):
    """
    Create Course Endpoint
    """
    data = request.data
    (
        course_details,
        course_curriculum,
        course_features,
        results_and_job_opportunities,
        exams_and_certifications,
        faqs,
        prerequisites,
    ) = (
        data["course_details"],
        data["course_curriculum"],
        data["course_features"],
        data["results_and_job_opportunities"],
        data["exams_and_certifications"],
        data["faqs"],
        data["prerequisites"],
    )

    course_details = json.loads(course_details)

    course_curriculum = json.loads(course_curriculum)
    pk = int(course_details["training"])
    course_features = json.loads(course_features)

    faqs = json.loads(faqs)
    exams_and_certifications = json.loads(exams_and_certifications)
    training = Training.objects.get(pk=pk)
    results_and_job_opportunities = json.loads(results_and_job_opportunities)
    prerequisites = json.loads(prerequisites)

    # Create course object in the database
    course = Course.objects.create(
        training=training,
        name=course_details["name"],
        tag=course_details["tag"],
        duration=course_details["duration"],
        overview=course_details["overview"],
        is_featured=bool(course_details["is_featured"]),
        is_live_on_website=course_details["is_live_on_website"],
        start_date=course_details["start_date"],
        image=request.FILES.get("image"),
    )

    # Create Topics and Subtopics for the above created course
    course = Course.objects.get(pk=course.id)
    for item in course_curriculum:
        if item["subtopic_of"] == None:
            topic = Topic.objects.create(
                course=course, id=int(item["id"]), title=item["title"], subtopic_of=None
            )
        else:
            topic = Topic.objects.get(pk=item["subtopic_of"])
            subtopic = Topic.objects.create(
                course=course,
                id=int(item["id"]),
                title=item["title"],
                subtopic_of=topic,
            )
    # Create course features for above created course.
    for item in course_features:
        feature = Feature.objects.create(course=course, name=item["name"])

    # Create Results and Job opportunities objects for the above created course.
    results_and_jobs = ResultsAndJobOpportunities.objects.create(
        course=course, description=results_and_job_opportunities["description"]
    )

    # Create Exam objects for the above created course.
    exams = ExamAndCertification.objects.create(
        course=course,
        description=exams_and_certifications["description"],
    )

    # Create FAQs for the above created course.
    for item in faqs:
        faq = FAQ.objects.create(faq=item["faq"], answer=item["answer"], course=course)

    # Create Prerequisites for the above created course.
    for item in prerequisites:
        pre = Prerequisite.objects.create(
            prerequisite=item["prerequisite"], course=course
        )
    response = {
        "status": "Success",
        "code": status.HTTP_201_CREATED,
        "message": "Course Created Successfully",
        "data": [],
    }

    return Response(response, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def createTopic(request):
    """Endpoint to create a new Topic."""
    data = request.data
    try:
        course = Course.objects.get(pk=data["course"])

        try:
            topic = Topic.objects.create(
                course=course,
                title=data["title"],
            )

            response = {
                "status": "Success",
                "code": status.HTTP_201_CREATED,
                "message": "Topic created successfully",
                "data": [],
            }

            return Response(response, status=status.HTTP_200_OK)

        except:
            response = {
                "status": "Failure",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid Payload",
                "data": [],
            }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Invalid course id",
            "data": [],
        }

        return Response(response, status=status.HTTP_404_NOT_FOUND)


@api_view(["PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def editCourse(request, pk):
    """
    Edit a course
    """
    try:
        course = Course.objects.get(pk=pk)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_404_NOT_FOUND,
            "message": "This Course Id Doesn't Exist",
            "data": [],
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    serializer = CourseCreationSerializer(course, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
    else:
        response = {
            "status": "Failure",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid Data",
            "data": [],
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "Course Updated Successfully",
        "data": [],
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def deleteCourse(request, pk):
    """Endpoint to delete a course."""
    try:
        course = Course.objects.get(pk=pk)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_404_NOT_FOUND,
            "message": "This Course Id Doesn't Exist",
            "data": [],
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    course.delete()
    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "Course Deleted Successfully!",
        "data": [],
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def editTraining(request, pk):
    """Endpoint to edit a Training."""
    data = request.data
    try:
        training = Training.objects.get(pk=pk)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_404_NOT_FOUND,
            "message": "This Training Id Doesn't Exist",
            "data": [],
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    serializer = TrainingSerializer(training, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()
    else:
        response = {
            "status": "Failure",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid Data",
            "data": [],
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "Course Updated Successfully",
        "data": [],
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def deleteTraining(request, pk):
    """Delete Training."""
    try:
        training = Training.objects.get(pk=pk)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Training Does Not Exist",
            "data": [],
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)

    training.delete()
    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "Training Deleted Successfully",
        "data": [],
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def enrollmentList(request):
    """List all Student Enrollments."""
    try:
        page_size = request.query_params["limit"]
    except:
        page_size = 10

    enrollments = Enrollment.objects.all().order_by("-date_and_time")
    try:
        param = request.query_params["q"]
    except:
        filterset = EnrollmentFilter(request.GET, queryset=enrollments)
        if filterset.is_valid():
            enrollments = filterset.qs
            paginator = PageNumberPagination()
            paginator.page_size = page_size
        result_page = paginator.paginate_queryset(enrollments, request)
        serializer = EnrollmentSerializer(
            result_page, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["q"]
    filtered_queryset = EnrollmentSearchFilter(request.GET, queryset=enrollments).qs
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    result_page = paginator.paginate_queryset(filtered_queryset, request)
    serializer = EnrollmentSerializer(
        result_page, many=True, context={"request": request}
    )

    return paginator.get_paginated_response(serializer.data)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def deleteEnrollment(request, pk):
    """Delete an enrollment entry."""
    try:
        enrollment = Enrollment.objects.get(pk=pk)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Enrollments ID Does Not Exist!",
            "data": [],
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)

    enrollment.delete()
    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "Enrollment Deleted Successfully",
        "data": [],
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def instructorEnquiries(request):
    """List all Instructor Enquiries."""
    try:
        page_size = request.query_params["limit"]
    except:
        page_size = 10
    enquiries = Instructor.objects.all().order_by("-date_and_time")

    try:
        param = request.query_params["q"]
    except:
        filterset = InstructorEnquiriesFilter(request.GET, queryset=enquiries)
        #     print(filterset)
        if filterset.is_valid():
            enquiries = filterset.qs
            paginator = PageNumberPagination()
            paginator.page_size = page_size
        result_page = paginator.paginate_queryset(enquiries, request)
        serializer = InstructorSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["q"]
    filtered_queryset = InstructorEnquiriesSearchFilter(
        request.GET, queryset=enquiries
    ).qs
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    result_page = paginator.paginate_queryset(filtered_queryset, request)
    serializer = InstructorSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def deleteInstructorQuery(request, pk):
    """Delete an Instructor Query."""
    try:
        query = Instructor.objects.get(pk=pk)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Query ID Does Not Exist",
            "data": [],
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    query.delete()
    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "Instructor Query Deleted Successfully",
        "data": [],
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def addInstructorQueryRemark(request, pk):
    """Add remark to instructor query."""
    data = request.data
    try:
        query = Instructor.objects.get(pk=pk)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Query ID Does Not Exist",
            "data": [],
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)

    serializer = InstructorSerializer(query, data=data, many=False, partial=True)
    if serializer.is_valid():
        serializer.save()

        response = {
            "status": "Success",
            "code": status.HTTP_200_OK,
            "message": "Remark Added Successfully",
            "data": [],
        }
        return Response(response, status=status.HTTP_200_OK)
    else:
        response = {
            "status": "Failure",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid Payload",
            "data": [],
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def equiriesList(request):
    """List all enquiries."""

    try:
        page_size = request.query_params["limit"]
    except:
        page_size = 10
    enquiries = Enquiry.objects.all().order_by("-requested_at")

    try:
        param = request.query_params["q"]
    except:
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(enquiries, request)
        serializer = EnquiryListSerializer(
            result_page, many=True, context={"request": request}
        )

        return paginator.get_paginated_response(serializer.data)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["q"]
    filtered_queryset = EnquiriesSearchFilter(request.GET, queryset=enquiries).qs
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    result_page = paginator.paginate_queryset(filtered_queryset, request)
    serializer = EnquiryListSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(["PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def addEquiriesRemark(request, pk):
    """Add remark to an Enquiry."""
    data = request.data
    try:
        enquiry = Enquiry.objects.get(pk=pk)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Query ID Does Not Exist",
            "data": [],
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)

    serializer = EnquiryEditSerializer(enquiry, data=data, many=False, partial=True)
    if serializer.is_valid():
        serializer.save()

        response = {
            "status": "Success",
            "code": status.HTTP_200_OK,
            "message": "Remark Added Successfully",
            "data": [],
        }
        return Response(response, status=status.HTTP_200_OK)
    else:
        response = {
            "status": "Failure",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid Payload",
            "data": [],
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def deleteCourseEnquiry(request, pk):
    """Delete a Course Enquiry."""
    try:
        enquiry = Enquiry.objects.get(pk=pk)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Equiry ID Does Not Exist",
            "data": [],
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)

    enquiry.delete()
    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "Enquiry Deleted Successfully",
        "data": [],
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def courseList(request):
    """
    Course List endpoint lists all the courses present on the site
    """
    try:
        page_size = request.query_params["limit"]
    except:
        page_size = 10
    course = Course.objects.all()

    try:
        param = request.query_params["q"]
        length = len(request.query_params["q"])
        print("Length: ", length)
        if length:
            filter_backends = [DjangoFilterBackend]
            filterset_fields = ["q"]
            filtered_queryset = CourseSearchFilter(request.GET, queryset=course).qs
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            result_page = paginator.paginate_queryset(filtered_queryset, request)
            serializer = CourseListSerializer(
                result_page, many=True, context={"request": request}
            )

        return paginator.get_paginated_response(serializer.data)

    except:
        filterset = CourseFilter(request.GET, queryset=course)

        if filterset.is_valid():
            course = filterset.qs
            paginator = PageNumberPagination()
            paginator.page_size = page_size
        result_page = paginator.paginate_queryset(course, request)
        serializer = CourseListSerializer(
            result_page, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def trainingList(request):
    """List all trainings."""
    try:
        page_size = request.query_params["limit"]
    except:
        page_size = 10

    trainings = Training.objects.all()
    try:
        param = request.query_params["q"]
        length = len(request.query_params["q"])
        print("Length: ", length)
        if length:
            filter_backends = [DjangoFilterBackend]
            filterset_fields = ["q"]
            filtered_queryset = TrainingSearchFilter(request.GET, queryset=trainings).qs
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            result_page = paginator.paginate_queryset(filtered_queryset, request)
            serializer = TrainingListSerializer(
                result_page, many=True, context={"request": request}
            )

        return paginator.get_paginated_response(serializer.data)
    except:
        filterset = TrainingFilter(request.GET, queryset=trainings)

        if filterset.is_valid():
            trainings = filterset.qs
            paginator = PageNumberPagination()
            paginator.page_size = page_size
        result_page = paginator.paginate_queryset(trainings, request)
        serializer = TrainingListSerializer(
            result_page, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def vendorList(request):
    """List all Vendors."""
    try:
        page_size = request.query_params["limit"]
    except:
        page_size = 10

    vendor = Vendor.objects.all()

    param = request.query_params["q"]
    length = len(request.query_params["q"])

    if length:
        filter_backends = [DjangoFilterBackend]
        filterset_fields = ["q"]
    filtered_queryset = VendorSearchFilter(request.GET, queryset=vendor).qs
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    result_page = paginator.paginate_queryset(filtered_queryset, request)
    serializer = VendorListSerializer(
        result_page, many=True, context={"request": request}
    )

    return paginator.get_paginated_response(serializer.data)


@api_view(["POST", "GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def FAQs(request):
    """List all FAQs related to the Website."""
    data = request.data
    if request.method == "POST":
        faq = ProductFAQ.objects.create(
            question=data["question"], answer=data["answer"]
        )

        response = {
            "status": "Success",
            "code": status.HTTP_201_CREATED,
            "message": "FAQ added Successfully",
            "data": [],
        }
        return Response(response, status=status.HTTP_201_CREATED)
    elif request.method == "GET":
        try:
            page_size = request.query_params["limit"]
        except:
            page_size = 10
        faqs = ProductFAQ.objects.all()

        try:
            param = request.query_params["q"]
        except:
            filterset = ProductFAQFilter(request.GET, queryset=faqs)
            if filterset.is_valid():
                faqs = filterset.qs
                paginator = PageNumberPagination()
                paginator.page_size = page_size
            result_page = paginator.paginate_queryset(faqs, request)
            serializer = ProductFAQListSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

        filter_backends = [DjangoFilterBackend]
        filterset_fields = ["q"]
        filtered_queryset = ProductFAQSearchFilter(request.GET, queryset=faqs).qs
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(filtered_queryset, request)
        serializer = ProductFAQListSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)


@api_view(["PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def editFAQ(request, pk):
    """Edit an FAQ related to the Website."""
    data = request.data
    try:
        faq = ProductFAQ.objects.get(pk=pk)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Invalid FAQ ID",
            "data": [],
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductFAQListSerializer(faq, data=data, many=False, partial=True)
    if serializer.is_valid():
        serializer.save()

        response = {
            "status": "Success",
            "code": status.HTTP_200_OK,
            "message": "FAQ Edited Successfully",
            "data": [],
        }

        return Response(response, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def deleteFAQ(request, pk):
    """Delete an FAQ"""
    try:
        faq = ProductFAQ.objects.get(pk=pk)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Invalid FAQ ID",
            "data": [],
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    faq.delete()
    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "FAQ Deleted Successfully!",
        "data": [],
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["POST", "GET", "PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def testimonials(request, pk=None):
    """Create, Edit, List testimonials."""
    data = request.data
    if request.method == "POST":
        testimonial = Testimonial.objects.create(
            message=data["message"], name=data["name"], designation=data["designation"]
        )
        response = {
            "status": "Success",
            "code": status.HTTP_201_CREATED,
            "message": "Testimonial Added Successfully",
            "data": [],
        }

        return Response(response, status=status.HTTP_201_CREATED)
    elif request.method == "GET":
        testimonials = Testimonial.objects.all()
        serializer = TestimonialSerializer(testimonials, many=True)

        response = {
            "status": "Success",
            "code": status.HTTP_200_OK,
            "message": "Testimonials fetched Successfully",
            "data": serializer.data,
        }

        return Response(response, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        try:
            testimonial = Testimonial.objects.get(pk=pk)
        except:
            response = {
                "status": "Failure",
                "code": status.HTTP_404_NOT_FOUND,
                "message": "Invalid Testimonial ID",
                "data": [],
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        serializer = TestimonialSerializer(
            testimonial, data=data, many=False, partial=True
        )
        if serializer.is_valid():
            serializer.save()

            response = {
                "status": "Success",
                "code": status.HTTP_200_OK,
                "message": "Testimonial Edited Successfully",
                "data": [],
            }

            return Response(response, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def deleteTestimonial(request, pk):
    """Delete a testimonial."""
    try:
        testimonial = Testimonial.objects.get(pk=pk)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Invalid Testimonial ID",
            "data": [],
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    testimonial.delete()
    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "Testimonial Deleted Successfully",
        "data": [],
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def contactQueries(request):
    """List all Contact Queries."""
    try:
        page_size = request.query_params["limit"]
    except:
        page_size = 10
    contacts = ContactUs.objects.all().order_by("-date_time")
    try:
        param = request.query_params["q"]
    except:
        filterset = ContactQueryFilter(request.GET, queryset=contacts)
        if filterset.is_valid():
            contacts = filterset.qs
            paginator = PageNumberPagination()
            paginator.page_size = page_size
        result_page = paginator.paginate_queryset(contacts, request)
        serializer = ContactQueriesSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["q"]
    filtered_queryset = ContactQuerySearchFilter(request.GET, queryset=contacts).qs
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    result_page = paginator.paginate_queryset(filtered_queryset, request)
    serializer = ContactQueriesSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def getcontactQuery(request, pk):
    """Retrieve a contact query detail."""
    try:
        query = ContactUs.objects.get(pk=pk)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Invalid Query ID",
            "data": [],
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    serializer = ContactQuerySerializer(query, many=False)

    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "Query fetched Successfully",
        "data": serializer.data,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def deleteContactQuery(request, pk):
    """Delete a contact query."""
    try:
        query = ContactUs.objects.get(pk=pk)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Invalid Query ID",
            "data": [],
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    query.delete()
    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "Contact Query Deleted Successfully!",
        "data": [],
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def emailSubscriberList(request):
    """
    Email Subscriber list with necessary filters
    """
    try:
        page_size = request.query_params["limit"]
    except:
        page_size = 10
    subscribers = EmailSubscriber.objects.all()
    try:
        param = request.query_params["q"]
    except:
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(subscribers, request)
        serializer = EmailSubscriberSerializer(
            result_page, many=True, context={"request": request}
        )

        return paginator.get_paginated_response(serializer.data)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["q"]
    filtered_queryset = EmailSubscriberSearchFilter(
        request.GET, queryset=subscribers
    ).qs
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    result_page = paginator.paginate_queryset(filtered_queryset, request)
    serializer = EmailSubscriberSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def deleteEmailSubscriber(request, pk):
    """Delete a Subscriber."""
    try:
        subscriber = EmailSubscriber.objects.get(pk=pk)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid Id",
            "data": [],
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    subscriber.delete()
    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "Subscriber Deleted Successfully!",
        "data": [],
    }
    return Response(response, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    """Change Password for the logged in user."""

    serializer_class = ChangePasswordSerializer
    model = CustomUser

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *agrs, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                response = {
                    "status": "Failure",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Wrong Password!",
                    "data": [],
                }
                return Response(
                    response,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def personalDetails(request):
    """Get personal details of the logged in AdminUser."""
    try:
        user = CustomUser.objects.get(pk=request.user.id)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "No User Found!",
            "data": [],
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    serializer = PersonalDetailsSerializer(user, many=False)
    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "Personal Details fetched Successfully",
        "data": serializer.data,
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def editPersonalDetails(request):
    """Edit personal details."""
    try:
        user = CustomUser.objects.get(pk=request.user.id)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "No User Found!",
            "data": [],
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    data = request.data

    serializer = PersonalDetailsSerializer(user, data=data, many=False, partial=True)
    if serializer.is_valid():
        serializer.save()
        response = {
            "status": "Success",
            "code": status.HTTP_200_OK,
            "message": "Personal Details Updated Successfully",
            "data": [],
        }
        return Response(response, status=status.HTTP_200_OK)

    else:
        response = {
            "status": "Failure",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": serializer.errors,
            "data": [],
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def contactDetails(request):
    """Get contact details for the logged in AdminUser."""
    try:
        user = CustomUser.objects.get(pk=request.user.id)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "No User Found!",
            "data": [],
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    serializer = ContactDetailsSerializer(user, many=False)
    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "Contact Details fetched Successfully",
        "data": serializer.data,
    }

    return Response(response, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def editContactDetails(request):
    """Edit contact details for the logged User."""
    try:
        user = CustomUser.objects.get(pk=request.user.id)
    except:
        response = {
            "status": "Failure",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "No User Found!",
            "data": [],
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    data = request.data

    serializer = ContactDetailsSerializer(user, data=data, many=False, partial=True)
    if serializer.is_valid():
        serializer.save()
        response = {
            "status": "Success",
            "code": status.HTTP_200_OK,
            "message": "Contact Details Updated Successfully",
            "data": [],
        }
        return Response(response, status=status.HTTP_200_OK)

    else:
        response = {
            "status": "Failure",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": serializer.errors,
            "data": [],
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def dailyCount(request):
    """Get daily count of enrollments, enqueries, instructor sign ups."""
    count = {}
    today = timezone.now().date()  # Get the current date
    enrollments = Enrollment.objects.filter(
        date_and_time__date=today
    )  # Filter enrollments by current date

    enrollment_count = enrollments.count()
    count["enrollments"] = enrollment_count

    course_enquiries = Enquiry.objects.filter(requested_at__date=today)
    course_enquiries_count = course_enquiries.count()
    count["course enquiries"] = course_enquiries_count

    instructor_enquiries = Instructor.objects.filter(date_and_time__date=today)
    instructor_enquiries_count = instructor_enquiries.count()
    count["instructor enquiries"] = instructor_enquiries_count

    contact_queries = ContactUs.objects.filter(date_time__date=today)
    contact_queries_count = contact_queries.count()
    count["contact queries"] = contact_queries_count

    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "Daily Count Fetched Successfully",
        "data": count,
    }

    return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def getAllVendors(request):
    """Get all vendors without Pagination."""
    vendors = Vendor.objects.all()
    serializer = VendorListSerializer(vendors, many=True)

    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "Vendors Fetched Successfully",
        "data": serializer.data,
    }

    return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsSuperUser])
def getAllTrainings(request):
    """Get all trainings without Pagination."""
    trainings = Training.objects.all()
    serializer = TrainingListSerializer(trainings, many=True)

    response = {
        "status": "Success",
        "code": status.HTTP_200_OK,
        "message": "Vendors Fetched Successfully",
        "data": serializer.data,
    }

    return Response(response, status=status.HTTP_200_OK)
