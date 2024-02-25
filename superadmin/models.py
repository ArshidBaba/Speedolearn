from django.db import models

from datetime import timezone

# Create your models here.
# from training.models import Course


class Vendor(models.Model):
    vendored = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="images/", blank=False, null=True)
    created_at = models.DateField(auto_now_add=True)
    is_live_on_website = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Training(models.Model):
    vendor = models.ForeignKey(
        Vendor, related_name="training_vendor", on_delete=models.CASCADE, null=True
    )
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to="images/", blank=False, null=True)
    live_on_website = models.CharField(max_length=150)
    tag = models.CharField(max_length=100, null=True)
    created_at = models.DateField(auto_now_add=True)
    is_featured = models.CharField(max_length=150)

    def __str__(self):
        return self.name


import io
from django.core.files.uploadedfile import InMemoryUploadedFile


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    training = models.ForeignKey(
        Training, related_name="course_training", on_delete=models.CASCADE, null=True
    )
    name = models.CharField(max_length=100)
    # price = models.FloatField()
    tag = models.CharField(
        max_length=100,
        null=True,
    )
    duration = models.CharField(max_length=10)
    overview = models.TextField(max_length=500, null=True)
    image = models.ImageField(upload_to="images/", blank=False, null=True)
    is_featured = models.CharField(max_length=10)
    is_live_on_website = models.CharField(max_length=10)
    start_date = models.DateField(null=True)
    # image = models.BinaryField(null=True)

    # def save(self, *args, **kwargs):
    #     if self.image and isinstance(self.image, InMemoryUploadedFile):
    #         image_bytes = io.BytesIO(self.image.read())
    #         self.image = image_bytes.getvalue()
    #     super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Topic(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    course = models.ForeignKey(
        Course, related_name="topic_course", on_delete=models.CASCADE, null=True
    )
    title = models.CharField(max_length=300)
    subtopic_of = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="subtopics",
    )

    # class Meta:
    #     verbose_name_plural = 'Topic'

    def __str__(self):
        return self.title


class Feature(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(
        Course, related_name="course_feature", null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name} of {self.course}"


class ResultsAndJobOpportunities(models.Model):
    description = models.TextField()
    course = models.OneToOneField(
        Course, related_name="course_results", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.course}'s Job Opportunity"


class JobImage(models.Model):
    # image = models.ImageField(upload_to="images/", blank=False, null=True)
    results_and_jobs = models.ForeignKey(
        ResultsAndJobOpportunities,
        related_name="job_images",
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.results_and_jobs}' Image"


class ExamAndCertification(models.Model):
    description = models.TextField()
    course = models.OneToOneField(
        Course, related_name="course_exam", on_delete=models.CASCADE, null=True
    )
    # certificate = models.ImageField(upload_to="images/", blank=False, null=True)

    def __str__(self):
        return f"{self.course}'s Exam & Certification"


class FAQ(models.Model):
    faq = models.TextField(max_length=200)
    answer = models.TextField(max_length=300)
    course = models.ForeignKey(
        Course, related_name="course_faq", null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.course}'s FAQ"


class ProductFAQ(models.Model):
    question = models.TextField(max_length=300)
    answer = models.TextField(max_length=300)

    def __str__(self):
        return f"{self.question}"


class Testimonial(models.Model):
    message = models.TextField(max_length=400)
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.designation} {self.name}'s Testimonial"


class Prerequisite(models.Model):
    course = models.ForeignKey(
        Course, related_name="course_prerequisite", on_delete=models.CASCADE
    )
    prerequisite = models.TextField(max_length=500)
