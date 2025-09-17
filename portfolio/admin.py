from django.contrib import admin
from .models import About, SocialLink, Experience, Project, Blog, Certification, Academic


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone")
    search_fields = ("full_name", "email")
    filter_horizontal = ("social_links",)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url")
    search_fields = ("platform",)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("experience_type", "role", "organization", "start_date", "end_date")
    list_filter = ("experience_type",)
    search_fields = ("role", "organization")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "tech_stack", "featured")
    list_filter = ("featured",)
    search_fields = ("title", "tech_stack")


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "url")
    search_fields = ("title", "subtitle")


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("title", "issuer")
    search_fields = ("title", "issuer")


@admin.register(Academic)
class AcademicAdmin(admin.ModelAdmin):
    list_display = ("institution", "degree", "date_range")
    search_fields = ("institution", "degree")

# Register your models here.
