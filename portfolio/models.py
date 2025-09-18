from django.db import models


class SocialLink(models.Model):
    platform = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self) -> str:
        return f"{self.platform}"


class About(models.Model):
    full_name = models.CharField(max_length=120)
    title = models.CharField(max_length=160, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=120, blank=True)
    summary = models.TextField(blank=True)
    photo = models.ImageField(upload_to="about_photos/", blank=True, null=True)
    roles_open_for = models.CharField(max_length=240, blank=True, help_text="Comma separated roles")

    social_links = models.ManyToManyField(SocialLink, blank=True)

    def __str__(self) -> str:
        return self.full_name


class Experience(models.Model):
    EXPERIENCE_TYPE_CHOICES = (
        ("internship", "Internship"),
        ("achievement", "Achievement/Award"),
        ("leadership", "Leadership/Workshop"),
    )

    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_TYPE_CHOICES, default="internship")
    organization = models.CharField(max_length=160)
    role = models.CharField(max_length=160)
    location = models.CharField(max_length=160, blank=True)
    start_date = models.CharField(max_length=60, blank=True)
    end_date = models.CharField(max_length=60, blank=True)
    bullets = models.TextField(blank=True, help_text="One per line")
    tech_stack = models.CharField(max_length=512, blank=True, help_text="Comma separated technologies used")

    class Meta:
        ordering = ["-start_date"]

    def __str__(self) -> str:
        return f"{self.role} @ {self.organization}"


class Project(models.Model):
    title = models.CharField(max_length=200)
    tech_stack = models.CharField(max_length=240, blank=True)
    description = models.TextField(blank=True)
    github_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    date_range = models.CharField(max_length=120, blank=True)
    role = models.CharField(
        max_length=60,
        blank=True,
        help_text="Primary role this project maps to (e.g., backend, genai, mlds, ux)",
    )

    def __str__(self) -> str:
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=240, blank=True)
    url = models.URLField()
    published_on = models.CharField(max_length=60, blank=True)

    def __str__(self) -> str:
        return self.title


class Certification(models.Model):
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=160)
    certificate_url = models.URLField(blank=True)

    def __str__(self) -> str:
        return f"{self.title} - {self.issuer}"


class Academic(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=240)
    location = models.CharField(max_length=160, blank=True)
    date_range = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True, help_text="One per line")

    def __str__(self) -> str:
        return f"{self.degree} — {self.institution}"

# Create your models here.
