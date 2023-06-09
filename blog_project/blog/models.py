from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Custom publish manager to retrive posts with PUBLISHED status.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
                      .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)

    # use unique_for_date param to ensure that slugs are
    # unique for the publication date
    # NOTE: not enforced at the database level
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')

    # this field defines many-to-one relationship
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')

    body = models.TextField()

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    class Meta:
        ordering = ['-publish']

    objects = models.Manager()      # The default manager.
    published = PublishedManager()  # The custom manager.

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
