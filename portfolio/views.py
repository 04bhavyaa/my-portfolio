import os
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.core.management import call_command
from .models import About, Experience, Project, Blog, Certification, Academic


def ensure_data_loaded():
    """Ensure data is loaded for Vercel's in-memory database"""
    if os.getenv('VERCEL'):
        try:
            # First run migrations to create tables
            call_command('migrate', '--run-syncdb')
            # Then load data if no data exists
            if not About.objects.exists():
                call_command('loaddata', 'portfolio/fixtures/initial_data.json')
        except Exception as e:
            print(f"Error setting up database: {e}")
            # If there's an error, try to create a minimal About object
            try:
                About.objects.get_or_create(
                    full_name="Bhavya Jha",
                    title="Data Science & Machine Learning Enthusiast",
                    email="bhavyajha1404@gmail.com",
                    summary="Passionate about creating innovative solutions and building meaningful projects.",
                    roles_open_for="Data Scientist, Machine Learning Engineer, Full Stack Developer"
                )
            except Exception as create_error:
                print(f"Error creating fallback data: {create_error}")


def home(request):
    # Ensure data is loaded for Vercel
    ensure_data_loaded()
    
    # Safely get data with fallbacks
    try:
        about = About.objects.first()
        roles_list = []
        if about and about.roles_open_for:
            roles_list = [r.strip() for r in about.roles_open_for.split(",") if r.strip()]
        internships = Experience.objects.filter(experience_type="internship")
        achievements = Experience.objects.filter(experience_type="achievement")
        leadership = Experience.objects.filter(experience_type="leadership")
        academics = Academic.objects.all()
        projects = Project.objects.all()
        blogs = Blog.objects.all()
        certifications = Certification.objects.all()
    except Exception as e:
        print(f"Error querying database: {e}")
        # Fallback data
        about = None
        roles_list = ["Data Scientist", "Machine Learning Engineer", "Full Stack Developer"]
        internships = []
        achievements = []
        leadership = []
        academics = []
        projects = []
        blogs = []
        certifications = []

    context = {
        "about": about,
        "roles_list": roles_list,
        "internships": internships,
        "achievements": achievements,
        "leadership": leadership,
        "projects": projects,
        "blogs": blogs,
        "certifications": certifications,
        "academics": academics,
    }
    return render(request, "portfolio/home.html", context)


def contact_submit(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        subject_line = request.POST.get("subject", "Portfolio Contact")
        email = request.POST.get("email", "")
        message = request.POST.get("message", "")
        composed = f"From: {name} <{email}>\n\n{message}"
        send_mail(
            subject=f"{subject_line}",
            message=composed,
            from_email=None,
            recipient_list=["bhavyajha1404@gmail.com"],
            fail_silently=False,
        )
        messages.success(request, "Thanks! Your message has been sent.")
        return redirect("home")
    return redirect("home")

# Create your views here.
