from django.db import models

from superadmin.models import Course


class Enquiry(models.Model):
    phone = models.CharField(max_length=10)
    requested_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(
        Course, related_name="course_enquiry", on_delete=models.CASCADE
    )
    remark = models.TextField(max_length=200, null=True)


class Enrollment(models.Model):
    course = models.ForeignKey(
        Course, related_name="course_enrollment", on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    date_and_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} enrolled to {self.course}"


class Instructor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    date_and_time = models.DateTimeField(auto_now_add=True)
    remark = models.TextField(max_length=200, null=True)


class ContactUs(models.Model):
    full_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    message = models.TextField(max_length=300)
    date_time = models.DateTimeField(auto_now_add=True)


class EmailSubscriber(models.Model):
    email = models.EmailField()
    date_and_time = models.DateTimeField(auto_now_add=True)
