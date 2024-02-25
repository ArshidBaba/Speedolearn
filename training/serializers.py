from rest_framework import serializers

from superadmin.models import (
    Course,
    Feature,
    Topic,
    Training,
    Vendor,
    ResultsAndJobOpportunities,
    ExamAndCertification,
    JobImage,
    FAQ,
    ProductFAQ,
    Testimonial,
    Prerequisite,
)
from .models import Enquiry, Enrollment


################################### SuperAdmin Serializers #####################################
class PrerequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prerequisite
        fields = ["id", "prerequisite"]


class JobImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobImage
        fields = "__all__"


class ExamAndCertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamAndCertification
        fields = "__all__"


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"


class ResultsAndJobOpportunitiesSerializer(serializers.ModelSerializer):
    images = JobImageSerializer(source="job_images", read_only=True, many=True)

    class Meta:
        model = ResultsAndJobOpportunities
        fields = "__all__"


class VendorListSerializer(serializers.ModelSerializer):
    course_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Vendor
        fields = "__all__"

    def get_course_count(self, obj):
        count = Course.objects.filter(training__vendor__id=obj.id).count()
        return count


class TrainingListSerializer(serializers.ModelSerializer):
    course_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Training
        fields = ["id", "name", "tag", "vendor", "course_count", "is_featured", "image"]

    def get_course_count(self, obj):
        course_count = Course.objects.filter(training=obj.id).count()
        return course_count


class CourseListSerializer(serializers.ModelSerializer):
    training = serializers.SerializerMethodField(read_only=True)
    # training_id = serializers.SerializerMethodField(read_only=True)
    # vendor = serializers.SerializerMethodField(read_only=True)
    vendor = serializers.CharField(source="training.vendor.name")
    vendor_id = serializers.IntegerField(source="training.vendor.id")

    class Meta:
        model = Course
        # fields = ["id", "name", "price", "tag", "vendor_id", "vendor","training", "duration", "is_featured"]
        fields = "__all__"

    def get_training(self, obj):
        training = obj.training.name
        return training

    # def get_training_id(self, obj):
    #     training_id = obj.training.id
    #     return training_id
    # def get_vendor(self, obj):
    #     vendor = obj.training.vendor.name
    #     return vendor


# class SubTopicSerializer(serializers.ModelSerializer):
#     subtopics
#     class Meta:
#         model = Topics
#         fields = "__all__"


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"


class TopicListSerializer(serializers.ModelSerializer):
    subtopics = serializers.SerializerMethodField(read_only=True)
    topic_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Topic
        fields = ["id", "title", "topic_count", "subtopics"]
        # fields = "__all__"
        # depth = 1

    # def get_course(self, obj):
    #     course = obj.course.name
    #     return course

    def get_subtopics(self, obj):
        subtopics = Topic.objects.filter(subtopic_of=obj.id)
        # count = Topic.objects.filter(subtopic_of=obj.id).count()
        serializer = TopicListSerializer(subtopics, many=True)
        # # print(serializer.data)
        # data = {}
        # data = serializer.data
        # print(data)
        # if serializer.data:
        #     data["count"] = count
        return serializer.data

    def get_topic_count(self, obj):
        count = Topic.objects.filter(subtopic_of=obj.id).count()
        return count


class CourseDetailSerializer(serializers.ModelSerializer):
    # topics = TopicListSerializer(source="topic_course", many=True, read_only=True)
    training = serializers.SerializerMethodField(read_only=True)
    topics = serializers.SerializerMethodField(read_only=True)
    # course = serializers.CharField(source="training.vendor.name")
    prerequisites = PrerequisiteSerializer(
        source="course_prerequisite", many=True, read_only=True
    )
    features = FeatureSerializer(source="course_feature", many=True, read_only=True)
    results_and_jobs = ResultsAndJobOpportunitiesSerializer(source="course_results")
    faqs = FAQSerializer(source="course_faq", many=True, read_only=True)
    exams_and_certifications = ExamAndCertificationSerializer(
        source="course_exam", read_only=True
    )
    vendor = serializers.CharField(source="training.vendor.name")
    logo = serializers.ImageField(source="training.vendor.logo")
    # logo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "overview",
            "duration",
            "tag",
            "training",
            "vendor",
            "logo",
            "prerequisites",
            "features",
            "topics",
            "results_and_jobs",
            "faqs",
            "exams_and_certifications",
        ]
        # fields = "__all__"
        depth = 1

    def get_training(self, obj):
        training = obj.training.name
        return training

    def get_topics(self, obj):
        topics = Topic.objects.filter(subtopic_of=None).filter(course=obj.id)
        serializer = TopicListSerializer(topics, many=True)
        return serializer.data

    def get_logo(self, obj):
        # return self.context["request"].build_absolute_uri(obj.training.vendor.logo.url)
        if obj.logo:
            return self.context["request"].build_absolute_uri(obj.logo.url)
        else:
            return None


class ProductFAQListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFAQ
        fields = "__all__"


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = "__all__"


######################################### Client Training Serilaizers ###############################


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["id", "phone", "course", "requested_at"]
