from django.contrib import admin
from .models import Department, Center
from .models import Center, Department, Student, Fee, MarkList, Tc, Subject, InternalMark, Course, Attendance



# Inline classes for related models
class DepartmentInline(admin.StackedInline):
    model = Department
    extra = 1

class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1

class CourseInline(admin.TabularInline):
    model = Course
    extra = 1

class InternalMarkInline(admin.TabularInline):
    model = InternalMark
    extra = 1

# Register models with custom admin options
@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'description')
    search_fields = ('name', 'location')
    ordering = ('name',)
    inlines = [DepartmentInline]

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'center', 'description')
    search_fields = ('name',)
    list_filter = ('center',)
    ordering = ('center',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'reg_no', 'roll_no', 'sem', 'attendance')
    search_fields = ('name', 'reg_no', 'roll_no')
    list_filter = ('sem',)
    ordering = ('name',)
    filter_horizontal = ('courses',)  # Display courses field as multi-select

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'sem', 'sem_fee', 'exam_fee')
    search_fields = ('student__name',)
    list_filter = ('sem',)
    ordering = ('student',)

@admin.register(MarkList)
class MarkListAdmin(admin.ModelAdmin):
    list_display = ('name', 'student', 'folio_no', 'given_date')
    search_fields = ('name', 'student', 'folio_no')
    ordering = ('name',)

@admin.register(Tc)
class TcAdmin(admin.ModelAdmin):
    list_display = ('name', 'student', 'folio_no', 'given_date', 'qualified_year')
    search_fields = ('name', 'student', 'folio_no')
    ordering = ('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'semester')
    search_fields = ('name', 'code')
    list_filter = ('department',)
    ordering = ('department',)

@admin.register(InternalMark)
class InternalMarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks_obtained', 'semester')
    search_fields = ('student__name', 'subject__name')
    list_filter = ('semester',)
    ordering = ('student',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'description')
    search_fields = ('name', 'code', 'department__name')
    list_filter = ('department',)
    ordering = ('name',)
    inlines = [SubjectInline]




@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'semester', 'classes_attended', 'total_classes', 'attendance_percentage_display')
    list_filter = ('course', 'semester')
    search_fields = ('student__name', 'student__reg_no', 'course__name')
    autocomplete_fields = ['student', 'course']
    readonly_fields = ('attendance_percentage_display',)

    def attendance_percentage_display(self, obj):
        return f"{obj.attendance_percentage:.2f}%"
    attendance_percentage_display.short_description = "Attendance Percentage"

# admin.site.register(Center, CenterAdmin)
# admin.site.register(Department, DepartmentAdmin)