from rest_framework import serializers
from .models import (
    ContactMessage, Service, Testimonial, HeroImage, PageImage, BlogPost, Update,
    AboutPage, AboutValue, AboutTimelineItem, ContactInformation,
    AboutStorySection, AboutMissionSection, AboutVisionSection,
    AboutValuesSection, AboutTimelineSection,
    BlogPostImage, BlogPostVideo, GalleryItem
)
from .utils import sanitize_html


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'phone', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_message(self, value):
        """Sanitize message content to prevent XSS"""
        return sanitize_html(value)
    
    def validate_subject(self, value):
        """Sanitize subject content to prevent XSS"""
        return sanitize_html(value)


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'service_type', 'icon', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'role', 'message', 'rating', 'is_featured', 'created_at']
        read_only_fields = ['id', 'created_at']


class HeroImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = HeroImage
        fields = ['id', 'title', 'image', 'image_url', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class PageImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = PageImage
        fields = ['id', 'page', 'title', 'image', 'image_url', 'section', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class BlogPostImageSerializer(serializers.ModelSerializer):
    """Serializer for blog post images"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPostImage
        fields = ['id', 'image', 'image_url', 'caption', 'alt_text', 'order', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class BlogPostVideoSerializer(serializers.ModelSerializer):
    """Serializer for blog post videos"""
    video_file_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    embed_url = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPostVideo
        fields = [
            'id', 'video_type', 'video_url', 'video_file', 'video_file_url',
            'title', 'thumbnail', 'thumbnail_url', 'embed_url', 'order', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_video_file_url(self, obj):
        if obj.video_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.video_file.url)
            return obj.video_file.url
        return None
    
    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.thumbnail.url)
            return obj.thumbnail.url
        return None
    
    def get_embed_url(self, obj):
        return obj.get_embed_url()


class BlogPostSerializer(serializers.ModelSerializer):
    featured_image_url = serializers.SerializerMethodField()
    images = BlogPostImageSerializer(many=True, read_only=True)
    videos = BlogPostVideoSerializer(many=True, read_only=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'category', 
            'author', 'featured_image', 'featured_image_url', 'published', 
            'created_date', 'updated_date', 'views', 'images', 'videos'
        ]
        read_only_fields = ['id', 'slug', 'created_date', 'updated_date', 'views']
    
    def validate_content(self, value):
        """Sanitize blog post content to prevent XSS"""
        return sanitize_html(value)
    
    def validate_excerpt(self, value):
        """Sanitize excerpt content to prevent XSS"""
        if value:
            return sanitize_html(value)
        return value
    
    def get_featured_image_url(self, obj):
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return obj.featured_image.url
        return None


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = [
            'id', 'title', 'content', 'type', 'priority', 
            'published', 'created_date', 'updated_date'
        ]
        read_only_fields = ['id', 'created_date', 'updated_date']


class AboutStorySectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutStorySection
        fields = ['id', 'title', 'content', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AboutMissionSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutMissionSection
        fields = ['id', 'title', 'content', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AboutVisionSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutVisionSection
        fields = ['id', 'title', 'content', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AboutValuesSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutValuesSection
        fields = ['id', 'title', 'subtitle', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AboutTimelineSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutTimelineSection
        fields = ['id', 'title', 'subtitle', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AboutValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutValue
        fields = ['id', 'icon', 'title', 'description', 'order', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AboutTimelineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutTimelineItem
        fields = ['id', 'year', 'title', 'description', 'order', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


# Legacy serializer for backward compatibility
class AboutPageSerializer(serializers.ModelSerializer):
    values = AboutValueSerializer(many=True, read_only=True)
    timeline_items = AboutTimelineItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = AboutPage
        fields = [
            'id', 'story_title', 'story_content', 'mission_title', 'mission_content',
            'vision_title', 'vision_content', 'values_title', 'values_subtitle',
            'timeline_title', 'timeline_subtitle', 'values', 'timeline_items',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ContactInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInformation
        fields = [
            'id', 'address_line1', 'address_line2', 'phone_primary', 'phone_secondary',
            'email_primary', 'email_secondary', 'hours_weekdays', 'hours_weekend',
            'facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class GalleryItemSerializer(serializers.ModelSerializer):
    """Serializer for gallery items (images and videos)"""
    image_url = serializers.SerializerMethodField()
    video_file_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    embed_url = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryItem
        fields = [
            'id', 'title', 'description', 'media_type', 'event_type', 'event_date',
            'image', 'image_url', 'video_type', 'video_url', 'video_file', 'video_file_url',
            'thumbnail', 'thumbnail_url', 'embed_url', 'is_featured', 'is_active',
            'order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def get_video_file_url(self, obj):
        if obj.video_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.video_file.url)
            return obj.video_file.url
        return None
    
    def get_thumbnail_url(self, obj):
        # If custom thumbnail exists, use it
        if obj.thumbnail:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.thumbnail.url)
            return obj.thumbnail.url
        
        # Generate thumbnail from YouTube URL
        if obj.media_type == 'video' and obj.video_type == 'youtube' and obj.video_url:
            from .utils import get_youtube_embed_url
            embed_url = get_youtube_embed_url(obj.video_url)
            if embed_url:
                # Extract video ID from embed URL
                video_id = embed_url.split('/embed/')[-1].split('?')[0]
                # Return YouTube thumbnail URL
                return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        
        # Generate thumbnail from Vimeo URL
        if obj.media_type == 'video' and obj.video_type == 'vimeo' and obj.video_url:
            from .utils import get_vimeo_embed_url
            embed_url = get_vimeo_embed_url(obj.video_url)
            if embed_url:
                # Extract video ID from embed URL
                video_id = embed_url.split('/video/')[-1]
                # Return Vimeo thumbnail URL using vumbnail service
                return f"https://vumbnail.com/{video_id}.jpg"
        
        return None
    
    def get_embed_url(self, obj):
        return obj.get_embed_url()
