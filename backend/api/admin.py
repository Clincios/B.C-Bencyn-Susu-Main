from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count, Q
from .models import (
    ContactMessage, Service, Testimonial, HeroImage, PageImage, BlogPost, Update,
    # AboutPage,  # Legacy model - removed from admin
    AboutValue, AboutTimelineItem, ContactInformation,
    AboutStorySection, AboutMissionSection, AboutVisionSection,
    AboutValuesSection, AboutTimelineSection,
    BlogPostImage, BlogPostVideo, GalleryItem
)

# ============================================================================
# CUSTOM ADMIN SITE CONFIGURATION
# ============================================================================

# Customize the default admin site
admin.site.site_header = "B.C BENCYN SUSU Administration"
admin.site.site_title = "BENCYN SUSU Admin"
admin.site.index_title = "Dashboard"
admin.site.site_url = "/"


# ============================================================================
# ADMIN PANEL ORGANIZATION
# ============================================================================
# Models are organized into logical groups:
# 1. 📧 COMMUNICATION - Contact Messages
# 2. 📝 CONTENT - Blog Posts, Updates, Services, Testimonials
# 3. 🖼️ MEDIA - Hero Images, Page Images, Blog Media
# 4. ℹ️ ABOUT PAGE - Unified About page management
# 5. 📞 CONTACT & SETTINGS - Contact Information
# ============================================================================


# ============================================================================
# 1. COMMUNICATION MANAGEMENT
# ============================================================================

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    list_editable = ['is_read']
    ordering = ['-created_at']
    list_per_page = 25
    
    fieldsets = (
        ('Message Details', {
            'fields': ('name', 'email', 'phone', 'subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f'{queryset.count()} message(s) marked as read.')
    mark_as_read.short_description = 'Mark selected messages as read'
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f'{queryset.count()} message(s) marked as unread.')
    mark_as_unread.short_description = 'Mark selected messages as unread'

    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = '📧 Contact Messages'


# ============================================================================
# 2. CONTENT MANAGEMENT
# ============================================================================

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'service_type', 'icon', 'is_active', 'created_at']
    list_filter = ['service_type', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    ordering = ['created_at']
    
    fieldsets = (
        ('Service Information', {
            'fields': ('title', 'description', 'service_type', 'icon')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at')
        }),
    )

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = '📝 Services'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'rating', 'is_featured', 'created_at']
    list_filter = ['rating', 'is_featured', 'created_at']
    search_fields = ['name', 'message', 'role']
    list_editable = ['is_featured']
    ordering = ['-created_at']
    list_per_page = 25
    
    fieldsets = (
        ('Testimonial Information', {
            'fields': ('name', 'role', 'message', 'rating')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'created_at'),
            'description': 'Featured testimonials will be displayed on the Home page'
        }),
    )
    
    actions = ['mark_as_featured', 'unmark_as_featured']
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f'{queryset.count()} testimonial(s) marked as featured.')
    mark_as_featured.short_description = 'Mark selected testimonials as featured'
    
    def unmark_as_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f'{queryset.count()} testimonial(s) unmarked as featured.')
    unmark_as_featured.short_description = 'Unmark selected testimonials as featured'

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = '⭐ Testimonials'


# ============================================================================
# BLOG POST INLINE MEDIA (Images and Videos)
# ============================================================================

class BlogPostImageInline(admin.TabularInline):
    """Inline admin for adding multiple images to a blog post"""
    model = BlogPostImage
    extra = 1
    fields = ['image', 'image_preview', 'caption', 'alt_text', 'order']
    readonly_fields = ['image_preview']
    ordering = ['order', 'created_at']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 80px; max-width: 120px; border-radius: 4px; object-fit: cover;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'


class BlogPostVideoInline(admin.TabularInline):
    """Inline admin for adding multiple videos to a blog post"""
    model = BlogPostVideo
    extra = 1
    fields = ['video_type', 'video_url', 'video_file', 'title', 'thumbnail', 'order']
    ordering = ['order', 'created_at']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'published', 'created_date', 'views', 'media_count', 'featured_image_preview']
    list_filter = ['category', 'published', 'created_date']
    search_fields = ['title', 'excerpt', 'content', 'author']
    readonly_fields = ['slug', 'created_date', 'updated_date', 'views', 'featured_image_preview']
    list_editable = ['published']
    date_hierarchy = 'created_date'
    ordering = ['-created_date']
    list_per_page = 25
    
    # Add inline media editors
    inlines = [BlogPostImageInline, BlogPostVideoInline]
    
    def save_model(self, request, obj, form, change):
        """Override save to handle file upload errors gracefully"""
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            from django.contrib import messages
            error_msg = f"Error saving blog post: {str(e)}"
            if hasattr(e, 'message'):
                error_msg = f"Error saving blog post: {e.message}"
            messages.error(request, error_msg)
            raise
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'excerpt', 'content'),
            'description': 'Enter the main blog post content. Add images and videos in the sections below.'
        }),
        ('Featured Image & Metadata', {
            'fields': ('category', 'author', 'featured_image', 'featured_image_preview'),
            'description': 'The featured image is displayed at the top of the blog post and in listing cards.'
        }),
        ('Publishing', {
            'fields': ('published', 'created_date', 'updated_date', 'views'),
            'description': 'Only published blog posts will be visible on the website'
        }),
    )
    
    def featured_image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 200px; border-radius: 4px;" />', obj.featured_image.url)
        return "No image"
    featured_image_preview.short_description = 'Featured Image Preview'
    
    def media_count(self, obj):
        """Display count of images and videos attached to the post"""
        images = obj.images.count()
        videos = obj.videos.count()
        parts = []
        if images:
            parts.append(f'📷 {images}')
        if videos:
            parts.append(f'🎬 {videos}')
        return ' | '.join(parts) if parts else '—'
    media_count.short_description = 'Media'

    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = '📝 Blog Posts'


# Remove standalone admins for BlogPostImage and BlogPostVideo
# They are now managed inline within BlogPost admin only
# This eliminates redundancy


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'priority', 'published', 'created_date']
    list_filter = ['type', 'priority', 'published', 'created_date']
    search_fields = ['title', 'content']
    readonly_fields = ['created_date', 'updated_date']
    list_editable = ['published']
    date_hierarchy = 'created_date'
    ordering = ['-created_date']
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'content')
        }),
        ('Metadata', {
            'fields': ('type', 'priority'),
            'description': 'Type: Announcement, Alert, News, or Event. Priority affects visual display on the Updates page.'
        }),
        ('Publishing', {
            'fields': ('published', 'created_date', 'updated_date'),
            'description': 'Only published updates will be visible on the website'
        }),
    )

    class Meta:
        verbose_name = 'Update'
        verbose_name_plural = '📝 Updates'


# ============================================================================
# 3. MEDIA MANAGEMENT
# ============================================================================

@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_preview', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title']
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    list_editable = ['is_active']
    list_per_page = 25
    ordering = ['-is_active', '-created_at']
    
    fieldsets = (
        ('Image Information', {
            'fields': ('title', 'image', 'image_preview'),
            'description': 'Hero images are displayed on the Home page. Only one active hero image will be shown. Recommended size: 1200x600px'
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'

    class Meta:
        verbose_name = 'Hero Image'
        verbose_name_plural = '🖼️ Hero Images'


@admin.register(PageImage)
class PageImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'page', 'section', 'image_preview', 'is_active', 'created_at']
    list_filter = ['page', 'is_active', 'created_at']
    search_fields = ['title', 'section']
    readonly_fields = ['image_preview', 'created_at', 'updated_at']
    list_editable = ['is_active']
    ordering = ['page', '-is_active', '-created_at']
    list_per_page = 25
    
    def save_model(self, request, obj, form, change):
        """Override save to handle file upload errors gracefully"""
        try:
            from .utils import validate_file_size
            if obj.image:
                validate_file_size(obj.image)
            super().save_model(request, obj, form, change)
        except Exception as e:
            from django.contrib import messages
            error_msg = f"Error saving page image: {str(e)}"
            if hasattr(e, 'message'):
                error_msg = f"Error saving page image: {e.message}"
            messages.error(request, error_msg)
            raise
    
    fieldsets = (
        ('Image Information', {
            'fields': ('title', 'image', 'image_preview'),
            'description': 'Upload an image for display on specific page sections'
        }),
        ('Page Assignment', {
            'fields': ('page', 'section'),
            'description': 'Select the page (Home, About, Services, Contact) and section identifier (e.g., "story", "header") where this image will be displayed.'
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'

    class Meta:
        verbose_name = 'Page Image'
        verbose_name_plural = '🖼️ Page Images'


# ============================================================================
# 4. UNIFIED ABOUT PAGE MANAGEMENT
# ============================================================================
# Consolidated admin interface for all About page content
# ============================================================================
# Note: AboutValue and AboutTimelineItem are independent models without
# ForeignKey relationships, so they cannot be managed inline.
# They are managed through their standalone admin pages.


# Unified About Page Admin - consolidates all About page sections
@admin.register(AboutStorySection)
class AboutStorySectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at', 'created_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    search_fields = ['title', 'content']
    
    fieldsets = (
        ('Story Content', {
            'fields': ('title', 'content'),
            'description': 'Main story content displayed on the About page'
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )

    class Meta:
        verbose_name = 'About Story Section'
        verbose_name_plural = 'ℹ️ About - Story'


@admin.register(AboutMissionSection)
class AboutMissionSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at', 'created_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    search_fields = ['title', 'content']
    
    fieldsets = (
        ('Mission Content', {
            'fields': ('title', 'content'),
            'description': 'Mission statement displayed on the About page'
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )

    class Meta:
        verbose_name = 'About Mission Section'
        verbose_name_plural = 'ℹ️ About - Mission'


@admin.register(AboutVisionSection)
class AboutVisionSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at', 'created_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    search_fields = ['title', 'content']
    
    fieldsets = (
        ('Vision Content', {
            'fields': ('title', 'content'),
            'description': 'Vision statement displayed on the About page'
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )

    class Meta:
        verbose_name = 'About Vision Section'
        verbose_name_plural = 'ℹ️ About - Vision'


@admin.register(AboutValuesSection)
class AboutValuesSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at', 'created_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    search_fields = ['title', 'subtitle']
    
    fieldsets = (
        ('Values Section Header', {
            'fields': ('title', 'subtitle'),
            'description': 'Header for the Values section. Manage individual values from the "About - Values" admin page.'
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )

    class Meta:
        verbose_name = 'About Values Section'
        verbose_name_plural = 'ℹ️ About - Values Header'


@admin.register(AboutTimelineSection)
class AboutTimelineSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at', 'created_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    search_fields = ['title', 'subtitle']
    
    fieldsets = (
        ('Timeline Section Header', {
            'fields': ('title', 'subtitle'),
            'description': 'Header for the Timeline section. Manage timeline items from the "About - Timeline Items" admin page.'
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )

    class Meta:
        verbose_name = 'About Timeline Section'
        verbose_name_plural = 'ℹ️ About - Timeline Header'


# Standalone admins for Values and Timeline Items (for direct access if needed)
@admin.register(AboutValue)
class AboutValueAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active', 'updated_at', 'created_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'description']
    ordering = ['order', 'id']
    
    fieldsets = (
        ('Value Information', {
            'fields': ('icon', 'title', 'description', 'order')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )

    class Meta:
        verbose_name = 'About Value'
        verbose_name_plural = 'ℹ️ About - Values'


@admin.register(AboutTimelineItem)
class AboutTimelineItemAdmin(admin.ModelAdmin):
    list_display = ['year', 'title', 'order', 'is_active', 'updated_at', 'created_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['order', 'is_active']
    search_fields = ['year', 'title', 'description']
    ordering = ['order', 'year']
    
    fieldsets = (
        ('Timeline Item Information', {
            'fields': ('year', 'title', 'description', 'order')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )

    class Meta:
        verbose_name = 'Timeline Item'
        verbose_name_plural = 'ℹ️ About - Timeline Items'


# Legacy AboutPage model - REMOVED FROM ADMIN
# Model kept in database for backward compatibility only
# Users should use the individual section admins instead:
# - About - Story Sections
# - About - Mission Sections
# - About - Vision Sections
# - About - Values Header (with inline values)
# - About - Timeline Header (with inline timeline items)
#
# @admin.register(AboutPage)
# class AboutPageAdmin(admin.ModelAdmin):
#     ... (removed to prevent usage of deprecated model)


# ============================================================================
# 5. CONTACT & SETTINGS MANAGEMENT
# ============================================================================

@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_active', 'email_primary', 'phone_primary', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    list_display_links = ['id']
    list_per_page = 10
    
    fieldsets = (
        ('Address Information', {
            'fields': ('address_line1', 'address_line2'),
            'description': 'Address information displayed on the Contact page and Footer'
        }),
        ('Phone Information', {
            'fields': ('phone_primary', 'phone_secondary'),
            'description': 'Primary and secondary phone numbers for contact'
        }),
        ('Email Information', {
            'fields': ('email_primary', 'email_secondary'),
            'description': 'Primary and secondary email addresses for contact'
        }),
        ('Business Hours', {
            'fields': ('hours_weekdays', 'hours_weekend'),
            'description': 'Business operating hours (e.g., "Monday - Friday: 8:00 AM - 6:00 PM")'
        }),
        ('Social Media Links', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url'),
            'description': 'Social media profile URLs. These links will appear in the footer with modern icons. Leave blank to hide a social media icon.'
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'description': 'Only active contact information will be displayed on the website'
        }),
    )

    class Meta:
        verbose_name = 'Contact Information'
        verbose_name_plural = '📞 Contact & Settings'


# ============================================================================
# 6. GALLERY MANAGEMENT
# ============================================================================

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'event_type', 'media_preview', 'is_featured', 'is_active', 'order', 'event_date', 'created_at']
    list_filter = ['media_type', 'event_type', 'is_featured', 'is_active', 'event_date', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at', 'image_preview', 'video_preview', 'thumbnail_preview']
    list_editable = ['is_featured', 'is_active', 'order']
    ordering = ['order', '-event_date', '-created_at']
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'media_type', 'event_type', 'event_date'),
            'description': 'Enter the title and description for this gallery item. Select the media type (Image or Video) and event type.'
        }),
        ('Image Settings', {
            'fields': ('image', 'image_preview'),
            'description': 'Upload an image for the gallery. This field is only used when Media Type is "Image".',
            'classes': ('collapse',)
        }),
        ('Video Settings', {
            'fields': ('video_type', 'video_url', 'video_file', 'thumbnail', 'thumbnail_preview', 'video_preview'),
            'description': 'Configure video settings. This section is only used when Media Type is "Video". You can use YouTube/Vimeo URLs or upload a video file.',
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active', 'order'),
            'description': 'Featured items will be displayed prominently. Only active items will be visible in the gallery.'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Override save to handle file upload errors gracefully"""
        try:
            from .utils import validate_file_size
            if obj.image:
                validate_file_size(obj.image)
            if obj.video_file:
                validate_file_size(obj.video_file)
            if obj.thumbnail:
                validate_file_size(obj.thumbnail)
            super().save_model(request, obj, form, change)
        except Exception as e:
            from django.contrib import messages
            error_msg = f"Error saving gallery item: {str(e)}"
            if hasattr(e, 'message'):
                error_msg = f"Error saving gallery item: {e.message}"
            messages.error(request, error_msg)
            raise
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px; border-radius: 4px; object-fit: cover;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Image Preview'
    
    def video_preview(self, obj):
        if obj.media_type == 'video':
            if obj.video_url:
                embed_url = obj.get_embed_url()
                if embed_url:
                    return format_html(
                        '<iframe src="{}" width="300" height="200" frameborder="0" allowfullscreen></iframe>',
                        embed_url
                    )
                return f"Video URL: {obj.video_url}"
            elif obj.video_file:
                return format_html(
                    '<video width="300" height="200" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>',
                    obj.video_file.url
                )
        return "No video"
    video_preview.short_description = 'Video Preview'
    
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="max-height: 80px; max-width: 120px; border-radius: 4px; object-fit: cover;" />',
                obj.thumbnail.url
            )
        return "No thumbnail"
    thumbnail_preview.short_description = 'Thumbnail Preview'
    
    def media_preview(self, obj):
        """Quick preview in list view"""
        if obj.media_type == 'image' and obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 80px; border-radius: 4px; object-fit: cover;" />',
                obj.image.url
            )
        elif obj.media_type == 'video':
            if obj.thumbnail:
                return format_html(
                    '<img src="{}" style="max-height: 50px; max-width: 80px; border-radius: 4px; object-fit: cover;" /> <span style="margin-left: 5px;">🎬</span>',
                    obj.thumbnail.url
                )
            return "🎬 Video"
        return "—"
    media_preview.short_description = 'Preview'

    class Meta:
        verbose_name = 'Gallery Item'
        verbose_name_plural = '🖼️ Gallery'
