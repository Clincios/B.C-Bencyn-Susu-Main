from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'services', views.ServiceViewSet, basename='service')
router.register(r'testimonials', views.TestimonialViewSet, basename='testimonial')
router.register(r'hero-images', views.HeroImageViewSet, basename='hero-image')
router.register(r'page-images', views.PageImageViewSet, basename='page-image')
router.register(r'blog-posts', views.BlogPostViewSet, basename='blog-post')
router.register(r'updates', views.UpdateViewSet, basename='update')
# Legacy endpoint removed - use individual section endpoints instead
# router.register(r'about-page', views.AboutPageViewSet, basename='about-page')
router.register(r'about-story', views.AboutStorySectionViewSet, basename='about-story')
router.register(r'about-mission', views.AboutMissionSectionViewSet, basename='about-mission')
router.register(r'about-vision', views.AboutVisionSectionViewSet, basename='about-vision')
router.register(r'about-values-header', views.AboutValuesSectionViewSet, basename='about-values-header')
router.register(r'about-timeline-header', views.AboutTimelineSectionViewSet, basename='about-timeline-header')
router.register(r'about-values', views.AboutValueViewSet, basename='about-value')
router.register(r'about-timeline-items', views.AboutTimelineItemViewSet, basename='about-timeline-item')
router.register(r'contact-information', views.ContactInformationViewSet, basename='contact-information')
router.register(r'gallery', views.GalleryItemViewSet, basename='gallery-item')

urlpatterns = [
    path('contact/', views.contact_create, name='contact-create'),
    path('contact/list/', views.contact_list, name='contact-list'),
    path('', include(router.urls)),
]
