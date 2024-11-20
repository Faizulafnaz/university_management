from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group
from django.utils import timezone
from academic_management.models import Department


class User(AbstractUser):

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('hod', 'Head of Department'),
        ('faculty', 'Faculty'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_verified = models.BooleanField(default=False) 

    def is_admin(self):
        return self.role == 'admin' or self.is_superuser
    
    def is_hod(self):
        return self.role == 'hod'
    
    def is_faculty(self):
        return self.role == 'faculty'



class Faculty(models.Model):

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    images = models.ImageField(upload_to="photos/profile")

    def __str__(self):
        return self.user.username


class Verification(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    faculty = models.OneToOneField(Faculty, on_delete=models.CASCADE, related_name='verification')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(blank=True)

    def approve(self):
        self.faculty.user.is_verified = True
        try:
            group = Group.objects.get(name='HOD')
            self.faculty.user.groups.add(group)
            self.faculty.user.is_staff = True
            self.faculty.user.save()
        except Group.DoesNotExist:
            print("HOD group does not exist.")


    def reject(self, comments=''):
        self.status = 'rejected'
        self.faculty.user.is_verified = False
        self.reviewed_at = timezone.now()
        self.comments = comments
        self.save()
        self.faculty.user.save()

    def is_pending(self):
        return self.status == 'pending'

    def __str__(self):
        return f"Verification status for {self.faculty.user.username}: {self.status}"


