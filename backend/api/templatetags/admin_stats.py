from django import template
from django.db.models import Count, Q
from ..models import ContactMessage, BlogPost, Service

register = template.Library()

@register.simple_tag
def get_contact_messages_count():
    return ContactMessage.objects.count()

@register.simple_tag
def get_unread_messages_count():
    return ContactMessage.objects.filter(is_read=False).count()

@register.simple_tag
def get_published_posts_count():
    return BlogPost.objects.filter(published=True).count()

@register.simple_tag
def get_active_services_count():
    return Service.objects.filter(is_active=True).count()

