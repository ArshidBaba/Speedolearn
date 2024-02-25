from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("login/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("create-vendor/", views.createVendor, name="create-vendor"),
    path("create-training/", views.createTraining, name="create-training"),
    path("create-course/", views.createCourse, name="create-course"),
    # path("create-topic/", views.createTopic, name="create-topic"),
    # path("topic/create-subtopic/", views.createSubtopic, name="create-subtopic"),
    path("edit-course/<int:pk>/", views.editCourse, name="edit-course"),
    # path(
    #     "course/<int:pk>/create-features/",
    #     views.addCourseFeatures,
    #     name="create-features",
    # ),
    path("delete-training/<int:pk>/", views.deleteTraining, name="delete-training"),
    path("enrollments/", views.enrollmentList, name="Enrollments-list"),
    path("instructor-queries/", views.instructorEnquiries, name="instructor-enquiries"),
    path("enquiries/", views.equiriesList, name="enquiries"),
    path("courses/", views.courseList, name="course-list"),
    path("trainings/", views.trainingList, name="training-list"),
    path("vendors/", views.vendorList, name="vendor-list"),
    path("faqs/", views.FAQs, name="add-faq"),
    path("edit-faq/<int:pk>/", views.editFAQ, name="edit-FAQ"),
    path("testimonials/", views.testimonials, name="create-testimonial"),
    path("testimonials/<int:pk>/", views.testimonials, name="edit-testimonial"),
    path("contact-queries/", views.contactQueries, name="contact-queries"),
    path("contact-query/<int:pk>/", views.getcontactQuery, name="contact-query"),
    path("subscribers/", views.emailSubscriberList, name="subscribers"),
    path(
        "add-instructor-remark/<int:pk>/",
        views.addInstructorQueryRemark,
        name="add-remark",
    ),
    path(
        "add-course-enquiry-remark/<int:pk>/",
        views.addEquiriesRemark,
        name="add-remark",
    ),
    path("edit-vendor/<int:pk>/", views.editVendor, name="edir-vendor"),
    path("delete-vendor/<int:pk>/", views.deleteVendor, name="delete-vendor"),
    path(
        "change-password/", views.ChangePasswordView.as_view(), name="change-password"
    ),
    path("personal-details/", views.personalDetails, name="personal-details"),
    path("contact-details/", views.contactDetails, name="contact-details"),
    path(
        "delete-subscriber/<int:pk>/",
        views.deleteEmailSubscriber,
        name="delete-subscriber",
    ),
    path("delete-FAQ/<int:pk>/", views.deleteFAQ, name="delete-FAQ"),
    path(
        "delete-contact-query/<int:pk>/",
        views.deleteContactQuery,
        name="delete-conatct-query",
    ),
    path(
        "delete-instructor-query/<int:pk>/",
        views.deleteInstructorQuery,
        name="delete-instructor-query",
    ),
    path(
        "delete-testimonial/<int:pk>/",
        views.deleteTestimonial,
        name="delete-testimonial",
    ),
    path("delete-course/<int:pk>/", views.deleteCourse, name="delete-course"),
    path(
        "delete-enrollment/<int:pk>/", views.deleteEnrollment, name="delete-enrollment"
    ),
    path("delete-enquiry/<int:pk>/", views.deleteCourseEnquiry, name="delete-enquiry"),
    path("daily-count/", views.dailyCount, name="daily-count"),
    path(
        "update-personal-details/",
        views.editPersonalDetails,
        name="edit-personal-details",
    ),
    path(
        "update-contact-details/", views.editContactDetails, name="edit-contact-details"
    ),
    path("edit-training/<int:pk>/", views.editTraining, name="edit-training"),
    path("get-all-vendors/", views.getAllVendors, name="get-all-vendors"),
    path("get-all-trainings/", views.getAllTrainings, name="get-all-trainings"),
]
