from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_read']),
        ]

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Service(models.Model):
    SERVICE_TYPES = [
        ('susu', 'Susu Collection'),
        ('savings', 'Savings Plans'),
        ('advisory', 'Financial Advisory'),
        ('loans', 'Loan Services'),
        ('group', 'Group Susu'),
        ('digital', 'Digital Services'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    icon = models.CharField(max_length=10, default='💰')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Testimonial'
        verbose_name_plural = '⭐ Testimonials'
        indexes = [
            models.Index(fields=['is_featured']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.name} - {self.rating} stars"


class HeroImage(models.Model):
    """Hero section image for homepage"""
    title = models.CharField(max_length=200, default='Hero Image')
    image = models.ImageField(
        upload_to='hero_images/',
        help_text='Upload an image for the hero section (recommended: 1200x600px)',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]
    )
    is_active = models.BooleanField(default=True, help_text='Only one active hero image will be displayed')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_active', '-created_at']
        verbose_name = 'Hero Image'
        verbose_name_plural = '🖼️ Hero Images'
        indexes = [
            models.Index(fields=['is_active', '-created_at']),
        ]

    def __str__(self):
        return f"{self.title} - {'Active' if self.is_active else 'Inactive'}"


class PageImage(models.Model):
    """Generic page images for different sections"""
    PAGE_CHOICES = [
        ('home', 'Home Page'),
        ('about', 'About Page'),
        ('services', 'Services Page'),
        ('contact', 'Contact Page'),
    ]
    
    page = models.CharField(max_length=20, choices=PAGE_CHOICES)
    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='page_images/',
        help_text='Upload an image for this page section',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]
    )
    section = models.CharField(
        max_length=50,
        help_text='Section identifier (e.g., "hero", "about-story", "services-header")',
        blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['page', '-is_active', '-created_at']
        verbose_name = 'Page Image'
        verbose_name_plural = 'Page Images'
        indexes = [
            models.Index(fields=['page', 'is_active']),
            models.Index(fields=['page', 'section']),
        ]

    def __str__(self):
        return f"{self.get_page_display()} - {self.title}"


class BlogPost(models.Model):
    """Blog post model for news and articles"""
    CATEGORY_CHOICES = [
        ('Financial Tips', 'Financial Tips'),
        ('Company News', 'Company News'),
        ('Savings Guide', 'Savings Guide'),
        ('Investment', 'Investment'),
        ('Community', 'Community'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt = models.TextField(max_length=500, blank=True, help_text='Short description of the post')
    content = models.TextField(help_text='Full blog post content')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Company News')
    author = models.CharField(max_length=100, blank=True)
    featured_image = models.ImageField(
        upload_to='blog_images/',
        blank=True,
        null=True,
        help_text='Featured image for the blog post',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]
    )
    published = models.BooleanField(default=False, help_text='Only published posts will be visible')
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        indexes = [
            models.Index(fields=['published', '-created_date']),
            models.Index(fields=['category', 'published']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Ensure slug uniqueness
            while BlogPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class BlogPostImage(models.Model):
    """Additional images for blog posts - displayed within the content"""
    blog_post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='blog_content_images/',
        help_text='Upload an image to include in the blog post',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'gif'])]
    )
    caption = models.CharField(max_length=300, blank=True, help_text='Optional caption for the image')
    alt_text = models.CharField(max_length=200, blank=True, help_text='Alt text for accessibility')
    order = models.IntegerField(default=0, help_text='Display order (lower numbers appear first)')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Blog Post Image'
        verbose_name_plural = 'Blog Post Images'

    def __str__(self):
        return f"Image for: {self.blog_post.title} (Order: {self.order})"


class BlogPostVideo(models.Model):
    """Videos for blog posts - supports YouTube, Vimeo, and uploaded videos"""
    VIDEO_TYPE_CHOICES = [
        ('youtube', 'YouTube'),
        ('vimeo', 'Vimeo'),
        ('upload', 'Uploaded Video'),
    ]
    
    blog_post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='videos'
    )
    video_type = models.CharField(
        max_length=20,
        choices=VIDEO_TYPE_CHOICES,
        default='youtube',
        help_text='Select the type of video'
    )
    video_url = models.URLField(
        blank=True,
        help_text='YouTube or Vimeo URL (e.g., https://www.youtube.com/watch?v=xxxxx or https://vimeo.com/xxxxx)',
        validators=[]
    )
    video_file = models.FileField(
        upload_to='blog_videos/',
        blank=True,
        null=True,
        help_text='Upload a video file (MP4, WebM, or OGG)',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'ogg'])]
    )
    title = models.CharField(max_length=200, blank=True, help_text='Video title')
    thumbnail = models.ImageField(
        upload_to='blog_video_thumbnails/',
        blank=True,
        null=True,
        help_text='Optional custom thumbnail for the video',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]
    )
    order = models.IntegerField(default=0, help_text='Display order (lower numbers appear first)')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Blog Post Video'
        verbose_name_plural = 'Blog Post Videos'

    def __str__(self):
        return f"Video for: {self.blog_post.title} ({self.get_video_type_display()})"
    
    def get_embed_url(self):
        """Convert video URL to embed URL for YouTube and Vimeo"""
        from .utils import get_video_embed_url
        return get_video_embed_url(self.video_url, self.video_type) or self.video_url


class Update(models.Model):
    """Company updates, announcements, alerts, and news"""
    TYPE_CHOICES = [
        ('announcement', 'Announcement'),
        ('alert', 'Alert'),
        ('news', 'News'),
        ('event', 'Event'),
    ]
    
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField(help_text='Update content')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='announcement')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
    published = models.BooleanField(default=False, help_text='Only published updates will be visible')
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Update'
        verbose_name_plural = 'Updates'
        indexes = [
            models.Index(fields=['published', '-created_date']),
            models.Index(fields=['type', 'published']),
            models.Index(fields=['priority', 'published']),
        ]

    def __str__(self):
        return f"{self.title} - {self.get_type_display()}"


# About Page Section Models - Each section can be managed independently

class AboutStorySection(models.Model):
    """Story section of the About page - can be managed independently"""
    title = models.CharField(max_length=200, default='Our Story')
    content = models.TextField(help_text='Main story content for the About page')
    is_active = models.BooleanField(default=True, help_text='Only active content will be displayed')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'About Story Section'
        verbose_name_plural = 'About - Story Sections'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['is_active', '-updated_at']),
        ]

    def __str__(self):
        return f"Story Section - {'Active' if self.is_active else 'Inactive'}"


class AboutMissionSection(models.Model):
    """Mission section of the About page - can be managed independently"""
    title = models.CharField(max_length=200, default='Our Mission')
    content = models.TextField(help_text='Mission statement')
    is_active = models.BooleanField(default=True, help_text='Only active content will be displayed')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'About Mission Section'
        verbose_name_plural = 'About Mission Sections'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['is_active', '-updated_at']),
        ]

    def __str__(self):
        return f"Mission Section - {'Active' if self.is_active else 'Inactive'}"


class AboutVisionSection(models.Model):
    """Vision section of the About page - can be managed independently"""
    title = models.CharField(max_length=200, default='Our Vision')
    content = models.TextField(help_text='Vision statement')
    is_active = models.BooleanField(default=True, help_text='Only active content will be displayed')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'About Vision Section'
        verbose_name_plural = 'About - Vision Sections'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['is_active', '-updated_at']),
        ]

    def __str__(self):
        return f"Vision Section - {'Active' if self.is_active else 'Inactive'}"


class AboutValuesSection(models.Model):
    """Values section header - manages the title and subtitle for the values section"""
    title = models.CharField(max_length=200, default='Our Core Values')
    subtitle = models.TextField(blank=True, help_text='Subtitle for values section')
    is_active = models.BooleanField(default=True, help_text='Only active content will be displayed')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'About Values Section Header'
        verbose_name_plural = 'About - Values Headers'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['is_active', '-updated_at']),
        ]

    def __str__(self):
        return f"Values Section Header - {'Active' if self.is_active else 'Inactive'}"


class AboutTimelineSection(models.Model):
    """Timeline section header - manages the title and subtitle for the timeline section"""
    title = models.CharField(max_length=200, default='Our Journey')
    subtitle = models.TextField(blank=True, help_text='Subtitle for timeline section')
    is_active = models.BooleanField(default=True, help_text='Only active content will be displayed')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'About Timeline Section Header'
        verbose_name_plural = 'About - Timeline Headers'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['is_active', '-updated_at']),
        ]

    def __str__(self):
        return f"Timeline Section Header - {'Active' if self.is_active else 'Inactive'}"


class AboutValue(models.Model):
    """Individual values for the About page - now independent"""
    icon = models.CharField(max_length=10, default='🎯', help_text='Emoji or icon identifier')
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField(default=0, help_text='Display order')
    is_active = models.BooleanField(default=True, help_text='Only active values will be displayed')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'About Value'
        verbose_name_plural = 'About - Values'
        indexes = [
            models.Index(fields=['is_active', 'order']),
        ]

    def __str__(self):
        return self.title


class AboutTimelineItem(models.Model):
    """Timeline items for the About page - now independent"""
    year = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0, help_text='Display order')
    is_active = models.BooleanField(default=True, help_text='Only active timeline items will be displayed')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'year']
        verbose_name = 'Timeline Item'
        verbose_name_plural = 'About - Timeline Items'
        indexes = [
            models.Index(fields=['is_active', 'order']),
        ]

    def __str__(self):
        return f"{self.year} - {self.title}"


# Keep old AboutPage model for backward compatibility during migration
# This will be removed in a future migration after data is migrated
class AboutPage(models.Model):
    """Legacy About page model - kept for migration purposes"""
    story_title = models.CharField(max_length=200, default='Our Story')
    story_content = models.TextField(help_text='Main story content for the About page')
    mission_title = models.CharField(max_length=200, default='Our Mission')
    mission_content = models.TextField(help_text='Mission statement')
    vision_title = models.CharField(max_length=200, default='Our Vision')
    vision_content = models.TextField(help_text='Vision statement')
    values_title = models.CharField(max_length=200, default='Our Core Values')
    values_subtitle = models.TextField(blank=True, help_text='Subtitle for values section')
    timeline_title = models.CharField(max_length=200, default='Our Journey')
    timeline_subtitle = models.TextField(blank=True, help_text='Subtitle for timeline section')
    is_active = models.BooleanField(default=True, help_text='Only active content will be displayed')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'About Page (Legacy)'
        verbose_name_plural = '📄 About - Legacy (Deprecated)'
        ordering = ['-updated_at']

    def __str__(self):
        return f"About Page Content - {'Active' if self.is_active else 'Inactive'}"


class ContactInformation(models.Model):
    """Contact information for the website"""
    # Address
    address_line1 = models.CharField(max_length=200, blank=True)
    address_line2 = models.CharField(max_length=200, blank=True, help_text='City, Country')
    
    # Phone
    phone_primary = models.CharField(max_length=20, blank=True)
    phone_secondary = models.CharField(max_length=20, blank=True)
    
    # Email
    email_primary = models.EmailField(blank=True)
    email_secondary = models.EmailField(blank=True)
    
    # Business Hours
    hours_weekdays = models.CharField(max_length=100, blank=True, help_text='e.g., Monday - Friday: 8:00 AM - 6:00 PM')
    hours_weekend = models.CharField(max_length=100, blank=True, help_text='e.g., Saturday: 9:00 AM - 2:00 PM')
    
    # Social Media Links
    facebook_url = models.URLField(max_length=200, blank=True, help_text='Facebook page URL')
    twitter_url = models.URLField(max_length=200, blank=True, help_text='Twitter/X profile URL')
    instagram_url = models.URLField(max_length=200, blank=True, help_text='Instagram profile URL')
    linkedin_url = models.URLField(max_length=200, blank=True, help_text='LinkedIn profile URL')
    
    is_active = models.BooleanField(default=True, help_text='Only active contact info will be displayed')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contact Information'
        verbose_name_plural = 'Contact Information'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['is_active', '-updated_at']),
        ]

    def __str__(self):
        return f"Contact Information - {'Active' if self.is_active else 'Inactive'}"


class GalleryItem(models.Model):
    """Gallery items for events - supports both images and videos"""
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    EVENT_TYPE_CHOICES = [
        ('meeting', 'Meeting'),
        ('celebration', 'Celebration'),
        ('workshop', 'Workshop'),
        ('community', 'Community Event'),
        ('award', 'Award Ceremony'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200, help_text='Title for the gallery item')
    description = models.TextField(blank=True, help_text='Optional description of the event or item')
    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPE_CHOICES,
        default='image',
        help_text='Select whether this is an image or video'
    )
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPE_CHOICES,
        default='other',
        help_text='Type of event this media is from'
    )
    
    # Image fields
    image = models.ImageField(
        upload_to='gallery_images/',
        blank=True,
        null=True,
        help_text='Upload an image for the gallery',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'gif'])]
    )
    
    # Video fields
    video_type = models.CharField(
        max_length=20,
        choices=[('youtube', 'YouTube'), ('vimeo', 'Vimeo'), ('upload', 'Uploaded Video')],
        default='youtube',
        blank=True,
        help_text='Type of video (only for video media type)'
    )
    video_url = models.URLField(
        blank=True,
        help_text='YouTube or Vimeo URL (e.g., https://www.youtube.com/watch?v=xxxxx)',
        validators=[]
    )
    
    def clean(self):
        """Validate video URL format"""
        from django.core.exceptions import ValidationError
        from .utils import validate_video_url
        
        if self.video_url and self.video_type in ['youtube', 'vimeo']:
            try:
                validate_video_url(self.video_url, self.video_type)
            except ValidationError as e:
                raise ValidationError({'video_url': e.messages})
    
    video_file = models.FileField(
        upload_to='gallery_videos/',
        blank=True,
        null=True,
        help_text='Upload a video file (MP4, WebM, or OGG)',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'ogg'])]
    )
    thumbnail = models.ImageField(
        upload_to='gallery_video_thumbnails/',
        blank=True,
        null=True,
        help_text='Optional custom thumbnail for videos',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]
    )
    
    event_date = models.DateField(
        blank=True,
        null=True,
        help_text='Date when the event occurred'
    )
    is_featured = models.BooleanField(
        default=False,
        help_text='Featured items will be displayed prominently'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Only active items will be displayed in the gallery'
    )
    order = models.IntegerField(
        default=0,
        help_text='Display order (lower numbers appear first)'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-event_date', '-created_at']
        verbose_name = 'Gallery Item'
        verbose_name_plural = '🖼️ Gallery Items'
        indexes = [
            models.Index(fields=['is_active', 'order']),
            models.Index(fields=['media_type', 'is_active']),
            models.Index(fields=['is_featured', 'is_active']),
        ]

    def __str__(self):
        return f"{self.title} - {self.get_media_type_display()}"
    
    def clean(self):
        """Validate video URL format"""
        from django.core.exceptions import ValidationError
        from .utils import validate_video_url
        
        if self.media_type == 'video' and self.video_url and self.video_type in ['youtube', 'vimeo']:
            try:
                validate_video_url(self.video_url, self.video_type)
            except ValidationError as e:
                raise ValidationError({'video_url': e.messages})
    
    def save(self, *args, **kwargs):
        """Override save to validate video URL"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    def get_embed_url(self):
        """Convert video URL to embed URL for YouTube and Vimeo"""
        if self.media_type == 'video' and self.video_url:
            from .utils import get_video_embed_url
            return get_video_embed_url(self.video_url, self.video_type) or self.video_url
        return self.video_url
