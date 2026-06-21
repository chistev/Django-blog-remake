from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            counter = 1
            while Category.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('category_detail', args=[self.slug])

class Article(models.Model):
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title)

            original_slug = self.slug
            counter = 1
            while Article.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        
        # Always call parent save to actually save to database
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Returns the URL for this article
        # Alternative: reverse('article_detail', kwargs={'slug': self.slug})
        return reverse('article_detail', args=[self.slug])

