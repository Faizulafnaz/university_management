from django.db import models

# Create your models here.

class Center(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name='departments')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.center.name}"
    

class Course(models.Model):
    name = models.CharField(max_length=100) 
    code = models.CharField(max_length=20, unique=True) 
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses') 
    description = models.TextField(blank=True, null=True) 
    total_semester = models.IntegerField()
    

    def __str__(self):
        return f"{self.name} ({self.code})"


class Student(models.Model):
    reg_no = models.CharField(max_length=20, unique=True)
    roll_no = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    sem = models.IntegerField()
    attendance = models.IntegerField()
    courses = models.ManyToManyField(Course, related_name='students')

    def __str__(self):
        return f"{self.name} - {self.reg_no}"
    

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sem = models.IntegerField()
    sem_fee = models.DecimalField(max_digits=10, decimal_places=2)
    exam_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Fees for {self.student.name} - Semester {self.sem}"


class MarkList(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    folio_no = models.CharField(max_length=50)
    given_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.reg_no}"


class Tc(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    folio_no = models.CharField(max_length=50)
    given_date = models.DateField()
    qualified_year = models.IntegerField()

    def __str__(self):
        return f"TC - {self.name} ({self.reg_no})"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')
    semester = models.PositiveIntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class InternalMark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='internal_marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='internal_marks')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    semester = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} ({self.marks_obtained})"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance_records')
    semester = models.PositiveIntegerField()
    classes_attended = models.PositiveIntegerField()
    total_classes = models.PositiveIntegerField()

    class Meta:
        unique_together = ('student', 'course', 'semester')

    def __str__(self):
        return f"{self.student.name} - {self.course.name} (Semester {self.semester})"

    @property
    def attendance_percentage(self):
        if self.total_classes:
            return (self.classes_attended / self.total_classes) * 100
        return 0.0


class Stock(models.Model):
    item_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='stocks')

    def __str__(self):
        return f"{self.item_name} - {self.department.name} ({self.quantity})"
