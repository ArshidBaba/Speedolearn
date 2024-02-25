from django_filters import rest_framework as filters

from .models import Course


class CourseFilter(filters.FilterSet):
    training = filters.CharFilter(lookup_expr="icontains")
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Course
        fields = [
            "training__id",
            "name",
            "tag",
            "duration",
            "training__vendor__id",
            "training__name",
        ]
