from rest_framework import serializers

from training.models import Enquiry, Enrollment, Instructor, ContactUs, EmailSubscriber

from .models import (
    Course,
    Training,
    Topic,
    Feature,
    Vendor,
    ProductFAQ,
    Testimonial,
    FAQ,
)

from accounts.models import CustomUser

########################################## SuperAdmin Serializers ##############################


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"


class TopicCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ["id", "name"]


class CourseCreationSerializer(serializers.ModelSerializer):
    # is_featured = serializers.BooleanField(required=True)

    class Meta:
        model = Course
        fields = "__all__"
        # fields = [
        #     "id",
        #     "name",
        #     "training",
        #     "tag",
        #     "duration",
        #     "overview",
        #     "start_date",
        #     "is_featured",
        #     "is_live_on_website",
        # ]

    # image = serializers.SerializerMethodField()

    # class Meta:
    #     model = Course
    #     fields = (
    #         "id",
    #         "training",
    #         "name",
    #         "price",
    #         "tag",
    #         "duration",
    #         "overview",
    #         "image",
    #         "is_featured",
    #         "is_live_on_website",
    #         "start_date",
    #     )

    # def get_image(self, obj):
    #     return obj.image.tobytes() if obj.image else None


from django.urls import reverse

import base64
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile


class CourseListSerializer(serializers.ModelSerializer):
    training = serializers.SerializerMethodField(read_only=True)
    vendor = serializers.CharField(source="training.vendor.name")
    features = FeatureSerializer(source="course_feature", read_only=True, many=True)
    # image = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "duration",
            # "image",
            "vendor",
            "training",
            "tag",
            "is_featured",
            "features",
        ]

    def get_training(self, obj):
        training = obj.training.name
        return training

    # def get_image(self, obj):
    #     if obj.image:
    #         image_data = base64.b64decode(obj.image)
    #         image_file = ContentFile(image_data)
    #         return ImageFile(image_file, name="course_image.jpg")
    #     return None


class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = "__all__"


class TrainingListSerializer(serializers.ModelSerializer):
    vendor = serializers.SerializerMethodField(read_only=True)
    # vendor_logo = serializers.SerializerMethodField(read_only=True)
    vendor_logo = serializers.ImageField(source="vendor.logo")

    class Meta:
        model = Training
        fields = [
            "id",
            "name",
            "vendor",
            "live_on_website",
            "created_at",
            "image",
            "vendor_logo",
        ]

    def get_vendor(self, obj):
        vendor = obj.vendor.name
        return vendor

    # def get_vendor_logo(self, obj):
    #     vendor_logo = obj.vendor.logo
    #     return vendor_logo


class VendorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id", "name", "logo", "created_at", "is_live_on_website"]


class VendorEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"


class ProductFAQListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFAQ
        fields = "__all__"


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = "__all__"


class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class PersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "name", "email", "username", "password"]


class ContactDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "phone_number",
            "alt_phone_number",
            "address",
            "city",
            "state",
            "country",
            "pincode",
            # "latitude",
            # "longitude",
        ]


####################################### Client Training Serilaizers ################################


class EnrollmentSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Enrollment
        fields = "__all__"

    def get_course(self, obj):
        course = obj.course.name
        return course


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = "__all__"


class EnquiryListSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Enquiry
        fields = ["id", "phone", "course", "requested_at", "remark"]

    def get_course(self, obj):
        return obj.course.name


class EnquiryEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = "__all__"


class ContactQueriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ["id", "full_name", "email", "phone", "date_time", "message"]


class ContactQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"


class EmailSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSubscriber
        fields = "__all__"
