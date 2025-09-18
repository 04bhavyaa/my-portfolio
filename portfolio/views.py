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
            call_command('migrate', '--run-syncdb')
            if not About.objects.exists():
                call_command('loaddata', 'portfolio/fixtures/initial_data.json')
        except Exception as e:
            print(f"Error setting up database: {e}")
            try:
                About.objects.get_or_create(
                    full_name="Bhavya Jha",
                    title="Data Science & Machine Learning Enthusiast",
                    email="bhavyajha1404@gmail.com",
                    summary="Passionate about creating innovative solutions and building meaningful projects.",
                    roles_open_for="Data Scientist, Machine Learning Engineer, Full Stack Developer",
                )
            except Exception as create_error:
                print(f"Error creating fallback data: {create_error}")


def home(request):
    ensure_data_loaded()

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
        # Pre-split tech_stack into a list for the template
        for p in projects:
            p.tech_stack_list = [t.strip() for t in p.tech_stack.split(",") if t.strip()]
        # Pre-split internship tech_stack into a list for tags
        for e in internships:
            e.tech_stack_list = [t.strip() for t in (e.tech_stack or "").split(",") if t.strip()]

        blogs = Blog.objects.all()
        certifications = Certification.objects.all()

    except Exception as e:
        print(f"Error querying database: {e}")
        about = None
        roles_list = ["Data Scientist", "Machine Learning Engineer", "Full Stack Developer"]
        internships = achievements = leadership = academics = []
        projects = blogs = certifications = []

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
            subject=subject_line,
            message=composed,
            from_email=None,
            recipient_list=["bhavyajha1404@gmail.com"],
            fail_silently=False,
        )
        messages.success(request, "Thanks! Your message has been sent.")
        return redirect("home")
    return redirect("home")
