from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle
from django.db import models
from .models import (
    ContactMessage, Service, Testimonial, HeroImage, PageImage, BlogPost, Update,
    # AboutPage,  # Legacy model - removed from API
    AboutValue, AboutTimelineItem, ContactInformation,
    AboutStorySection, AboutMissionSection, AboutVisionSection,
    AboutValuesSection, AboutTimelineSection, GalleryItem
)
from .serializers import (
    ContactMessageSerializer, ServiceSerializer, TestimonialSerializer,
    HeroImageSerializer, PageImageSerializer, BlogPostSerializer, UpdateSerializer,
    # AboutPageSerializer,  # Legacy serializer - removed from API
    ContactInformationSerializer,
    AboutStorySectionSerializer, AboutMissionSectionSerializer, AboutVisionSectionSerializer,
    AboutValuesSectionSerializer, AboutTimelineSectionSerializer,
    AboutValueSerializer, AboutTimelineItemSerializer, GalleryItemSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])  # Explicitly allow public access for contact form
@throttle_classes([AnonRateThrottle])  # Rate limit to prevent spam/DoS attacks
def contact_create(request):
    """
    Create a new contact message.
    Public endpoint for contact form submissions.
    Rate limited to prevent spam and DoS attacks.
    """
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def contact_list(request):
    """
    List all contact messages (admin only).
    """
    messages = ContactMessage.objects.all()
    serializer = ContactMessageSerializer(messages, many=True)
    return Response(serializer.data)


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing services.
    Public read-only endpoint.
    """
    permission_classes = [AllowAny]  # Explicitly allow public read access
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer


class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing testimonials.
    Public read-only endpoint.
    """
    permission_classes = [AllowAny]  # Explicitly allow public read access
    queryset = Testimonial.objects.filter(is_featured=True)
    serializer_class = TestimonialSerializer


class HeroImageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing hero images.
    Returns only the most recent active hero image.
    Public read-only endpoint.
    """
    permission_classes = [AllowAny]  # Explicitly allow public read access
    serializer_class = HeroImageSerializer
    
    def get_queryset(self):
        # Return only the most recent active hero image
        return HeroImage.objects.filter(is_active=True).order_by('-created_at')[:1]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class PageImageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing page images.
    Public read-only endpoint.
    """
    permission_classes = [AllowAny]  # Explicitly allow public read access
    queryset = PageImage.objects.filter(is_active=True)
    serializer_class = PageImageSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        page = self.request.query_params.get('page', None)
        section = self.request.query_params.get('section', None)
        
        if page:
            queryset = queryset.filter(page=page)
        if section:
            queryset = queryset.filter(section=section)
        
        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing blog posts.
    Public read-only endpoint.
    """
    permission_classes = [AllowAny]  # Explicitly allow public read access
    queryset = BlogPost.objects.filter(published=True)
    serializer_class = BlogPostSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)
        
        if category and category != 'all':
            queryset = queryset.filter(category=category)
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) | 
                models.Q(excerpt__icontains=search)
            )
        
        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        return super().retrieve(request, *args, **kwargs)


class UpdateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing company updates.
    Public read-only endpoint.
    """
    permission_classes = [AllowAny]  # Explicitly allow public read access
    queryset = Update.objects.filter(published=True)
    serializer_class = UpdateSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        update_type = self.request.query_params.get('type', None)
        priority = self.request.query_params.get('priority', None)
        
        if update_type:
            queryset = queryset.filter(type=update_type)
        if priority:
            queryset = queryset.filter(priority=priority)
        
        return queryset


class AboutStorySectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing About Story section.
    Returns only the active story section.
    Public read-only endpoint.
    """
    permission_classes = [AllowAny]  # Explicitly allow public read access
    serializer_class = AboutStorySectionSerializer
    pagination_class = None
    
    def get_queryset(self):
        # Return only the most recent active story section (max 1 for safety)
        return AboutStorySection.objects.filter(is_active=True).order_by('-updated_at')[:1]


class AboutMissionSectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing About Mission section.
    Returns only the active mission section.
    Public read-only endpoint.
    """
    permission_classes = [AllowAny]  # Explicitly allow public read access
    serializer_class = AboutMissionSectionSerializer
    pagination_class = None
    
    def get_queryset(self):
        # Return only the most recent active mission section (max 1 for safety)
        return AboutMissionSection.objects.filter(is_active=True).order_by('-updated_at')[:1]


class AboutVisionSectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing About Vision section.
    Returns only the active vision section.
    Public read-only endpoint.
    """
    permission_classes = [AllowAny]  # Explicitly allow public read access
    serializer_class = AboutVisionSectionSerializer
    pagination_class = None
    
    def get_queryset(self):
        # Return only the most recent active vision section (max 1 for safety)
        return AboutVisionSection.objects.filter(is_active=True).order_by('-updated_at')[:1]


class AboutValuesSectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing About Values section header.
    Returns only the active values section header.
    Public read-only endpoint.
    """
    permission_classes = [AllowAny]  # Explicitly allow public read access
    serializer_class = AboutValuesSectionSerializer
    pagination_class = None
    
    def get_queryset(self):
        # Return only the most recent active values section header (max 1 for safety)
        return AboutValuesSection.objects.filter(is_active=True).order_by('-updated_at')[:1]


class AboutTimelineSectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing About Timeline section header.
    Returns only the active timeline section header.
    Public read-only endpoint.
    """
    permission_classes = [AllowAny]  # Explicitly allow public read access
    serializer_class = AboutTimelineSectionSerializer
    pagination_class = None
    
    def get_queryset(self):
        # Return only the most recent active timeline section header (max 1 for safety)
        return AboutTimelineSection.objects.filter(is_active=True).order_by('-updated_at')[:1]


class AboutValueViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing About Values.
    Returns all active values.
    Public read-only endpoint.
    """
    permission_classes = [AllowAny]  # Explicitly allow public read access
    serializer_class = AboutValueSerializer
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        # Return all active values ordered by display order
        return AboutValue.objects.filter(is_active=True).order_by('order', 'id')


class AboutTimelineItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing About Timeline Items.
    Returns all active timeline items.
    Public read-only endpoint.
    """
    permission_classes = [AllowAny]  # Explicitly allow public read access
    serializer_class = AboutTimelineItemSerializer
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        # Return all active timeline items ordered by display order
        return AboutTimelineItem.objects.filter(is_active=True).order_by('order', 'year')


# Legacy AboutPageViewSet - REMOVED
# The AboutPage model is deprecated. Use individual section endpoints instead:
# - /api/about-story/
# - /api/about-mission/
# - /api/about-vision/
# - /api/about-values-header/
# - /api/about-timeline-header/
# - /api/about-values/
# - /api/about-timeline-items/
#
# class AboutPageViewSet(viewsets.ReadOnlyModelViewSet):
#     ... (removed to prevent usage of deprecated endpoint)


class ContactInformationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing Contact Information.
    Returns only the active contact information.
    Public read-only endpoint.
    """
    permission_classes = [AllowAny]  # Explicitly allow public read access
    serializer_class = ContactInformationSerializer
    pagination_class = None  # Disable pagination for this endpoint
    
    def get_queryset(self):
        # Return only the most recent active contact information (max 1 for safety)
        return ContactInformation.objects.filter(is_active=True).order_by('-updated_at')[:1]


class GalleryItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing gallery items (images and videos).
    Public read-only endpoint.
    """
    permission_classes = [AllowAny]  # Explicitly allow public read access
    serializer_class = GalleryItemSerializer
    queryset = GalleryItem.objects.filter(is_active=True)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        media_type = self.request.query_params.get('media_type', None)
        event_type = self.request.query_params.get('event_type', None)
        featured = self.request.query_params.get('featured', None)
        
        if media_type:
            queryset = queryset.filter(media_type=media_type)
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)
        
        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
