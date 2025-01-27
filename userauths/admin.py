from django.contrib import admin

from userauths.models import User, Profile

class UserAdmin(admin.ModelAdmin):
    search_fields =[ "full_name", "username"]
    list_display = ["full_name", "username", "email", "phone_number", "gender"]

class ProfileAdmin(admin.ModelAdmin):
    search_fields =[ "full_name", "user__username"]
    list_display = ["full_name", "user", "verified"]


# Register your models here.
