# Generated migration for adding database indexes and validation improvements

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_galleryitem'),
    ]

    operations = [
        # Add indexes to ContactMessage
        migrations.AddIndex(
            model_name='contactmessage',
            index=models.Index(fields=['-created_at'], name='api_contact_created_idx'),
        ),
        migrations.AddIndex(
            model_name='contactmessage',
            index=models.Index(fields=['is_read'], name='api_contact_is_read_idx'),
        ),
        # Add indexes to Service
        migrations.AddIndex(
            model_name='service',
            index=models.Index(fields=['is_active'], name='api_service_is_active_idx'),
        ),
        migrations.AddIndex(
            model_name='service',
            index=models.Index(fields=['created_at'], name='api_service_created_idx'),
        ),
        # Add indexes to Testimonial
        migrations.AddIndex(
            model_name='testimonial',
            index=models.Index(fields=['is_featured'], name='api_testimonial_featured_idx'),
        ),
        migrations.AddIndex(
            model_name='testimonial',
            index=models.Index(fields=['-created_at'], name='api_testimonial_created_idx'),
        ),
        # Add indexes to HeroImage
        migrations.AddIndex(
            model_name='heroimage',
            index=models.Index(fields=['is_active', '-created_at'], name='api_heroimage_active_created_idx'),
        ),
        # Add indexes to PageImage
        migrations.AddIndex(
            model_name='pageimage',
            index=models.Index(fields=['page', 'is_active'], name='api_pageimage_page_active_idx'),
        ),
        migrations.AddIndex(
            model_name='pageimage',
            index=models.Index(fields=['page', 'section'], name='api_pageimage_page_section_idx'),
        ),
        # Add indexes to BlogPost
        migrations.AddIndex(
            model_name='blogpost',
            index=models.Index(fields=['published', '-created_date'], name='api_blogpost_published_created_idx'),
        ),
        migrations.AddIndex(
            model_name='blogpost',
            index=models.Index(fields=['category', 'published'], name='api_blogpost_category_published_idx'),
        ),
        migrations.AddIndex(
            model_name='blogpost',
            index=models.Index(fields=['slug'], name='api_blogpost_slug_idx'),
        ),
        # Add indexes to Update
        migrations.AddIndex(
            model_name='update',
            index=models.Index(fields=['published', '-created_date'], name='api_update_published_created_idx'),
        ),
        migrations.AddIndex(
            model_name='update',
            index=models.Index(fields=['type', 'published'], name='api_update_type_published_idx'),
        ),
        migrations.AddIndex(
            model_name='update',
            index=models.Index(fields=['priority', 'published'], name='api_update_priority_published_idx'),
        ),
        # Add indexes to About sections
        migrations.AddIndex(
            model_name='aboutstorysection',
            index=models.Index(fields=['is_active', '-updated_at'], name='api_aboutstory_active_updated_idx'),
        ),
        migrations.AddIndex(
            model_name='aboutmissionsection',
            index=models.Index(fields=['is_active', '-updated_at'], name='api_aboutmission_active_updated_idx'),
        ),
        migrations.AddIndex(
            model_name='aboutvisionsection',
            index=models.Index(fields=['is_active', '-updated_at'], name='api_aboutvision_active_updated_idx'),
        ),
        migrations.AddIndex(
            model_name='aboutvaluessection',
            index=models.Index(fields=['is_active', '-updated_at'], name='api_aboutvaluessection_active_updated_idx'),
        ),
        migrations.AddIndex(
            model_name='abouttimelinesection',
            index=models.Index(fields=['is_active', '-updated_at'], name='api_abouttimelinesection_active_updated_idx'),
        ),
        # Add indexes to AboutValue
        migrations.AddIndex(
            model_name='aboutvalue',
            index=models.Index(fields=['is_active', 'order'], name='api_aboutvalue_active_order_idx'),
        ),
        # Add indexes to AboutTimelineItem
        migrations.AddIndex(
            model_name='abouttimelineitem',
            index=models.Index(fields=['is_active', 'order'], name='api_abouttimelineitem_active_order_idx'),
        ),
        # Add indexes to ContactInformation
        migrations.AddIndex(
            model_name='contactinformation',
            index=models.Index(fields=['is_active', '-updated_at'], name='api_contactinfo_active_updated_idx'),
        ),
        # Add indexes to GalleryItem
        migrations.AddIndex(
            model_name='galleryitem',
            index=models.Index(fields=['is_active', 'order'], name='api_galleryitem_active_order_idx'),
        ),
        migrations.AddIndex(
            model_name='galleryitem',
            index=models.Index(fields=['media_type', 'is_active'], name='api_galleryitem_media_active_idx'),
        ),
        migrations.AddIndex(
            model_name='galleryitem',
            index=models.Index(fields=['is_featured', 'is_active'], name='api_galleryitem_featured_active_idx'),
        ),
    ]

