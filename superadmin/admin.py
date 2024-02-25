from django.contrib import admin

from .models import (
    Vendor,
    Training,
    Course,
    Topic,
    Feature,
    ExamAndCertification,
    # ExamImage,
    ResultsAndJobOpportunities,
    JobImage,
    FAQ,
    ProductFAQ,
    Testimonial,
    Prerequisite,
)

# Register your models here.
admin.site.register(Vendor)
admin.site.register(Training)
admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(Feature)
admin.site.register(FAQ)
admin.site.register(ExamAndCertification)
admin.site.register(ResultsAndJobOpportunities)
admin.site.register(JobImage)
admin.site.register(ProductFAQ)
admin.site.register(Testimonial)
admin.site.register(Prerequisite)


class ModelOptions(admin.ModelAdmin):
    fieldsets = (
        (
            "",
            {
                "fields": (
                    "title",
                    "subtitle",
                    "slug",
                    "pub_date",
                    "status",
                ),
            },
        ),
        (
            "Flags",
            {
                "classes": ("grp-collapse grp-closed",),
                "fields": (
                    "flag_front",
                    "flag_sticky",
                    "flag_allow_comments",
                    "flag_comments_closed",
                ),
            },
        ),
        (
            "Tags",
            {
                "classes": ("grp-collapse grp-open",),
                "fields": ("tags",),
            },
        ),
    )


class StackedItemInline(admin.StackedInline):
    classes = ("grp-collapse grp-open",)


class TabularItemInline(admin.TabularInline):
    classes = ("grp-collapse grp-open",)
