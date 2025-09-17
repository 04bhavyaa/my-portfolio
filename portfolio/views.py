from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import About, Experience, Project, Blog, Certification, Academic


def home(request):
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
