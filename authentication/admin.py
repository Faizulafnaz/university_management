from django.contrib import admin
from .models import User, Faculty, Verification
from django.contrib import messages 
from django.shortcuts import redirect
from django.contrib.messages import get_messages
# Register your models here.



class VerificationAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'status', 'submitted_at', 'reviewed_at', 'comments')  
    list_filter = ('status', 'submitted_at')  
    search_fields = ('user__username', 'user__email') 

    def get_queryset(self, request):
        # Only show verifications to admin
        if request.user.is_admin():
            return super().get_queryset(request)
        return Verification.objects.none()


class FacultyInline(admin.StackedInline):
    model = Faculty
    can_delete = False
    verbose_name_plural = 'Faculty Details'
    fk_name = 'user'

class CustomUserAdmin(admin.ModelAdmin):
    inlines = (FacultyInline,)
    list_display = ('username', 'email', 'role', 'is_verified')
    list_filter = ('role', 'is_verified')
    search_fields = ('username', 'email')
    ordering = ('username',)

    # Restricting access for non-admin users
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # HOD can only view faculty users
        if request.user.is_authenticated and request.user.role == 'hod':
            return qs.filter(role='faculty')
        return qs

    # Making certain fields read-only or hidden based on role
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_authenticated and request.user.role == 'hod':
            form.base_fields['role'].initial = 'faculty'
            form.base_fields['role'].disabled = True
        return form

    def save_related(self, request, form, formsets, change):
        # Save related objects (like Faculty inline)
        super().save_related(request, form, formsets, change)

        # Validate if the Faculty object was created for users with the 'faculty' role
        obj = form.instance 
        if obj.role == 'faculty':
            try:
                faculty = Faculty.objects.get(user=obj)
                # If Faculty object exists, show a success message
                self.message_user(request, "Faculty details created successfully.", level=messages.SUCCESS)
            except Faculty.DoesNotExist:
                # If the Faculty object doesn't exist, show an error message
                obj.delete()
                self.message_user(request, "Error: Faculty details were not created. Please check the form.", level=messages.ERROR)
    
    def response_add(self, request, obj, post_url_continue=None):
        # Check if the user was deleted (because Faculty creation failed)
        if not obj.pk:
            # User was deleted, override the default success message
            self.message_user(request, "Error: User could not be created because Faculty details were missing. User has been deleted.", level=messages.ERROR)
            # Preserve form data
            return redirect(request.path)

        return super().response_add(request, obj, post_url_continue)
    
    def save_model(self, request, obj, form, change):
    
        if obj.password:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

                




admin.site.register(User, CustomUserAdmin)
admin.site.register(Verification, VerificationAdmin)


