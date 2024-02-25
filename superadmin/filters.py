import django_filters as d_filters
from django.db.models import Q

from django_filters import rest_framework as filters

from .models import Course, FAQ, Training, Vendor
from training.models import EmailSubscriber, ContactUs, Instructor, Enrollment, Enquiry


class CourseFilter(filters.FilterSet):
    training = filters.CharFilter()
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Course
        fields = [
            "training",
            "name",
            "tag",
            "duration",
            "training__vendor__id",
        ]


class CourseSearchFilter(d_filters.FilterSet):
    q = d_filters.CharFilter(method="search_all_fields")

    class Meta:
        model = Course
        fields = ["q"]

    def search_all_fields(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            | Q(training__name__icontains=value)
            | Q(tag__icontains=value)
            # | Q(id__icontains=value)
        )


class ProductFAQSearchFilter(d_filters.FilterSet):
    q = d_filters.CharFilter(method="search_all_fields")

    class Meta:
        model = FAQ
        fields = ["q"]

    def search_all_fields(self, queryset, name, value):
        return queryset.filter(
            Q(question__icontains=value)
            | Q(answer__icontains=value)
            # | Q(course__name__icontains=value)
        )


class ProductFAQFilter(filters.FilterSet):
    id = filters.NumberFilter()
    # name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Course
        fields = ["id"]


class EmailSubscriberSearchFilter(d_filters.FilterSet):
    q = d_filters.CharFilter(method="search_all_fields")

    class Meta:
        model = EmailSubscriber
        fields = ["q"]

    def search_all_fields(self, queryset, name, value):
        return queryset.filter(
            Q(email__icontains=value)
            # | Q(answer__icontains=value)
            # | Q(course__name__icontains=value)
        )


class ContactQueryFilter(filters.FilterSet):
    # training = filters.CharFilter()
    # full_name = filters.CharFilter(lookup_expr="icontains")

    # class Meta:
    #     model = ContactUs
    #     fields = [
    #         "training",
    #         "name",
    #         "tag",
    #         "duration",
    #         "training__vendor__id",
    #     ]
    pass


class ContactQuerySearchFilter(d_filters.FilterSet):
    q = d_filters.CharFilter(method="search_all_fields")

    class Meta:
        model = ContactUs
        fields = ["q"]

    def search_all_fields(self, queryset, name, value):
        return queryset.filter(
            Q(full_name__icontains=value)
            | Q(email__icontains=value)
            | Q(phone__icontains=value)
            # | Q(answer__icontains=value)
            # | Q(course__name__icontains=value)
        )


class InstructorEnquiriesSearchFilter(d_filters.FilterSet):
    q = d_filters.CharFilter(method="search_all_fields")

    class Meta:
        model = Instructor
        fields = ["q"]

    def search_all_fields(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            | Q(email__icontains=value)
            | Q(phone__icontains=value)
        )


class InstructorEnquiriesFilter(filters.FilterSet):
    pass


class TrainingSearchFilter(d_filters.FilterSet):
    q = d_filters.CharFilter(method="search_all_fields")

    class Meta:
        model = Training
        fields = ["q"]

    def search_all_fields(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            | Q(vendor__name__icontains=value)
            | Q(tag__icontains=value)
        )


class TrainingFilter(filters.FilterSet):
    vendor = filters.NumberFilter()
    # name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Course
        fields = ["vendor"]


class EnrollmentSearchFilter(d_filters.FilterSet):
    q = d_filters.CharFilter(method="search_all_fields")

    class Meta:
        model = Enrollment
        fields = ["q"]

    def search_all_fields(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            | Q(email__icontains=value)
            | Q(course__name__icontains=value)
        )


class EnrollmentFilter(filters.FilterSet):
    pass


class EnquiriesSearchFilter(d_filters.FilterSet):
    q = d_filters.CharFilter(method="search_all_fields")

    class Meta:
        model = Enquiry
        fields = ["q"]

    def search_all_fields(self, queryset, name, value):
        return queryset.filter(
            Q(course__name__icontains=value)
            # | Q(email__icontains=value)
            | Q(phone__icontains=value)
        )


class EnquiriesFilter(filters.FilterSet):
    pass


class VendorSearchFilter(d_filters.FilterSet):
    q = d_filters.CharFilter(method="search_all_fields")

    class Meta:
        model = Vendor
        fields = ["q"]

    def search_all_fields(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            # | Q(training__name__icontains=value)
            # | Q(tag__icontains=value)
            # | Q(id__icontains=value)
        )
