# Generated manually for About Page, Values, Timeline, and Contact Information

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_update'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story_title', models.CharField(default='Our Story', max_length=200)),
                ('story_content', models.TextField(help_text='Main story content for the About page')),
                ('mission_title', models.CharField(default='Our Mission', max_length=200)),
                ('mission_content', models.TextField(help_text='Mission statement')),
                ('vision_title', models.CharField(default='Our Vision', max_length=200)),
                ('vision_content', models.TextField(help_text='Vision statement')),
                ('values_title', models.CharField(default='Our Core Values', max_length=200)),
                ('values_subtitle', models.TextField(blank=True, help_text='Subtitle for values section')),
                ('timeline_title', models.CharField(default='Our Journey', max_length=200)),
                ('timeline_subtitle', models.TextField(blank=True, help_text='Subtitle for timeline section')),
                ('is_active', models.BooleanField(default=True, help_text='Only active content will be displayed')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'About Page',
                'verbose_name_plural': 'About Page',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='AboutValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(default='🎯', help_text='Emoji or icon identifier', max_length=10)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('order', models.IntegerField(default=0, help_text='Display order')),
                ('about_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='api.aboutpage')),
            ],
            options={
                'verbose_name': 'About Value',
                'verbose_name_plural': 'About Values',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='AboutTimelineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('order', models.IntegerField(default=0, help_text='Display order')),
                ('about_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timeline_items', to='api.aboutpage')),
            ],
            options={
                'verbose_name': 'Timeline Item',
                'verbose_name_plural': 'Timeline Items',
                'ordering': ['order', 'year'],
            },
        ),
        migrations.CreateModel(
            name='ContactInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line1', models.CharField(blank=True, max_length=200)),
                ('address_line2', models.CharField(blank=True, help_text='City, Country', max_length=200)),
                ('phone_primary', models.CharField(blank=True, max_length=20)),
                ('phone_secondary', models.CharField(blank=True, max_length=20)),
                ('email_primary', models.EmailField(blank=True, max_length=254)),
                ('email_secondary', models.EmailField(blank=True, max_length=254)),
                ('hours_weekdays', models.CharField(blank=True, help_text='e.g., Monday - Friday: 8:00 AM - 6:00 PM', max_length=100)),
                ('hours_weekend', models.CharField(blank=True, help_text='e.g., Saturday: 9:00 AM - 2:00 PM', max_length=100)),
                ('is_active', models.BooleanField(default=True, help_text='Only active contact info will be displayed')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Contact Information',
                'verbose_name_plural': 'Contact Information',
                'ordering': ['-updated_at'],
            },
        ),
    ]
