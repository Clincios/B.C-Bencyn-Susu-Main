"""
Utility functions for the API app.
"""
import re
from urllib.parse import urlparse
from django.core.exceptions import ValidationError
from django.conf import settings


def get_youtube_embed_url(video_url):
    """
    Convert YouTube URL to embed URL format.
    
    Args:
        video_url: YouTube URL in various formats
        
    Returns:
        Embed URL string or None if invalid
    """
    if not video_url:
        return None
    
    youtube_patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in youtube_patterns:
        match = re.search(pattern, video_url)
        if match:
            return f"https://www.youtube.com/embed/{match.group(1)}"
    
    return None


def get_vimeo_embed_url(video_url):
    """
    Convert Vimeo URL to embed URL format.
    
    Args:
        video_url: Vimeo URL
        
    Returns:
        Embed URL string or None if invalid
    """
    if not video_url:
        return None
    
    vimeo_match = re.search(r'vimeo\.com\/(\d+)', video_url)
    if vimeo_match:
        return f"https://player.vimeo.com/video/{vimeo_match.group(1)}"
    
    return None


def get_video_embed_url(video_url, video_type):
    """
    Convert video URL to embed URL based on video type.
    
    Args:
        video_url: Video URL
        video_type: 'youtube' or 'vimeo'
        
    Returns:
        Embed URL string or None if invalid
    """
    if video_type == 'youtube':
        return get_youtube_embed_url(video_url)
    elif video_type == 'vimeo':
        return get_vimeo_embed_url(video_url)
    
    return video_url


def validate_file_size(file):
    """
    Validate that uploaded file size is within limits.
    
    Args:
        file: Django UploadedFile object
        
    Raises:
        ValidationError if file is too large
    """
    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024)  # Default 10MB
    
    if file.size > max_size:
        max_size_mb = max_size / (1024 * 1024)
        raise ValidationError(
            f'File size exceeds maximum allowed size of {max_size_mb:.1f}MB.'
        )


def validate_video_url(video_url, video_type):
    """
    Validate video URL format based on video type.
    
    Args:
        video_url: Video URL string
        video_type: 'youtube' or 'vimeo'
        
    Returns:
        True if valid, False otherwise
        
    Raises:
        ValidationError if URL format is invalid
    """
    if not video_url:
        return True  # URL is optional
    
    # Basic URL validation
    try:
        parsed = urlparse(video_url)
        if not parsed.scheme or not parsed.netloc:
            raise ValidationError(f'Invalid URL format: {video_url}')
        
        # Validate scheme (must be http or https)
        if parsed.scheme not in ['http', 'https']:
            raise ValidationError(f'URL must use http or https protocol: {video_url}')
    except Exception as e:
        if isinstance(e, ValidationError):
            raise
        raise ValidationError(f'Invalid URL format: {video_url}')
    
    # Type-specific validation
    if video_type == 'youtube':
        youtube_patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        ]
        for pattern in youtube_patterns:
            if re.search(pattern, video_url):
                return True
        raise ValidationError(
            f'Invalid YouTube URL format. Expected formats: '
            f'https://www.youtube.com/watch?v=VIDEO_ID or https://youtu.be/VIDEO_ID'
        )
    
    elif video_type == 'vimeo':
        if re.search(r'vimeo\.com\/(\d+)', video_url):
            return True
        raise ValidationError(
            f'Invalid Vimeo URL format. Expected format: https://vimeo.com/VIDEO_ID'
        )
    
    return True


def sanitize_html(content):
    """
    Sanitize HTML content to prevent XSS attacks.
    
    Args:
        content: HTML string to sanitize
        
    Returns:
        Sanitized HTML string
    """
    try:
        import bleach
        # Allow basic formatting tags
        allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'ul', 'ol', 'li', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        allowed_attributes = {
            'a': ['href', 'title', 'target'],
        }
        return bleach.clean(content, tags=allowed_tags, attributes=allowed_attributes, strip=True)
    except ImportError:
        # If bleach is not installed, return content as-is (should not happen in production)
        return content

