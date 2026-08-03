from django.contrib import admin
from .models import *


# User admin 
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id","username", "role",)

# Register your models here.
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("id","user","interests",)
    

@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ("id","user","title",)
    
   
@admin.register(SponsorProfile)
class SponsorProfileAdmin(admin.ModelAdmin):
    list_display = ("id","user","company_name",)