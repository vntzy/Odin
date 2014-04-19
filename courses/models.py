from django.db import models
from tinymce import models as tinymce_models


class Course(models.Model):
    name = models.CharField(blank=False, max_length=64)
    short_description = models.CharField(blank=True, max_length=300)
    description = tinymce_models.HTMLField(blank=False)
    image = models.ImageField(upload_to="courses_logoes", null=True, blank=True)
    git_repository = models.CharField(blank=True, max_length=256)
    show_on_index = models.BooleanField(default=False)
    
    applications_url = models.URLField(null=True, blank=True)
    application_until = models.DateField()
    next_season_mail_list = models.URLField(null=True, blank=True)

    SEO_title = models.CharField(blank=False, max_length=255)
    SEO_description = models.CharField(blank=False, max_length=255)
    url = models.SlugField(max_length=80, unique=True)

    def __unicode__(self):
        return self.name
