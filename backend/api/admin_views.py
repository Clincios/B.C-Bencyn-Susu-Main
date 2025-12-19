from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms import ModelForm
from .models import (
    AboutStorySection, AboutMissionSection, AboutVisionSection,
    AboutValuesSection, AboutTimelineSection, AboutValue, AboutTimelineItem
)


class AboutStoryForm(ModelForm):
    class Meta:
        model = AboutStorySection
        fields = ['title', 'content', 'is_active']


class AboutMissionForm(ModelForm):
    class Meta:
        model = AboutMissionSection
        fields = ['title', 'content', 'is_active']


class AboutVisionForm(ModelForm):
    class Meta:
        model = AboutVisionSection
        fields = ['title', 'content', 'is_active']


class AboutValuesSectionForm(ModelForm):
    class Meta:
        model = AboutValuesSection
        fields = ['title', 'subtitle', 'is_active']


class AboutTimelineSectionForm(ModelForm):
    class Meta:
        model = AboutTimelineSection
        fields = ['title', 'subtitle', 'is_active']


@staff_member_required
def about_settings_view(request):
    """Consolidated About Settings page - manage all About page sections in one place"""
    
    # Get or create the most recent active sections
    story_section = AboutStorySection.objects.filter(is_active=True).order_by('-updated_at').first()
    if not story_section:
        story_section = AboutStorySection.objects.order_by('-updated_at').first()
    if not story_section:
        story_section = AboutStorySection()
    
    mission_section = AboutMissionSection.objects.filter(is_active=True).order_by('-updated_at').first()
    if not mission_section:
        mission_section = AboutMissionSection.objects.order_by('-updated_at').first()
    if not mission_section:
        mission_section = AboutMissionSection()
    
    vision_section = AboutVisionSection.objects.filter(is_active=True).order_by('-updated_at').first()
    if not vision_section:
        vision_section = AboutVisionSection.objects.order_by('-updated_at').first()
    if not vision_section:
        vision_section = AboutVisionSection()
    
    values_section = AboutValuesSection.objects.filter(is_active=True).order_by('-updated_at').first()
    if not values_section:
        values_section = AboutValuesSection.objects.order_by('-updated_at').first()
    if not values_section:
        values_section = AboutValuesSection()
    
    timeline_section = AboutTimelineSection.objects.filter(is_active=True).order_by('-updated_at').first()
    if not timeline_section:
        timeline_section = AboutTimelineSection.objects.order_by('-updated_at').first()
    if not timeline_section:
        timeline_section = AboutTimelineSection()
    
    # Get all values and timeline items
    values = AboutValue.objects.filter(is_active=True).order_by('order', 'id')
    timeline_items = AboutTimelineItem.objects.filter(is_active=True).order_by('order', 'year')
    
    if request.method == 'POST':
        section = request.POST.get('section')
        success = False
        
        if section == 'story':
            # Create new instance if it doesn't exist
            if not story_section.pk:
                story_section = AboutStorySection()
            form = AboutStoryForm(request.POST, instance=story_section)
            if form.is_valid():
                form.save()
                messages.success(request, 'Story section saved successfully!')
                success = True
        elif section == 'mission':
            # Create new instance if it doesn't exist
            if not mission_section.pk:
                mission_section = AboutMissionSection()
            form = AboutMissionForm(request.POST, instance=mission_section)
            if form.is_valid():
                form.save()
                messages.success(request, 'Mission section saved successfully!')
                success = True
        elif section == 'vision':
            # Create new instance if it doesn't exist
            if not vision_section.pk:
                vision_section = AboutVisionSection()
            form = AboutVisionForm(request.POST, instance=vision_section)
            if form.is_valid():
                form.save()
                messages.success(request, 'Vision section saved successfully!')
                success = True
        elif section == 'values_header':
            # Create new instance if it doesn't exist
            if not values_section.pk:
                values_section = AboutValuesSection()
            form = AboutValuesSectionForm(request.POST, instance=values_section)
            if form.is_valid():
                form.save()
                messages.success(request, 'Values section header saved successfully!')
                success = True
        elif section == 'timeline_header':
            # Create new instance if it doesn't exist
            if not timeline_section.pk:
                timeline_section = AboutTimelineSection()
            form = AboutTimelineSectionForm(request.POST, instance=timeline_section)
            if form.is_valid():
                form.save()
                messages.success(request, 'Timeline section header saved successfully!')
                success = True
        
        if success:
            return redirect('about_settings')
    
    # Initialize forms
    story_form = AboutStoryForm(instance=story_section)
    mission_form = AboutMissionForm(instance=mission_section)
    vision_form = AboutVisionForm(instance=vision_section)
    values_section_form = AboutValuesSectionForm(instance=values_section)
    timeline_section_form = AboutTimelineSectionForm(instance=timeline_section)
    
    context = {
        'story_form': story_form,
        'mission_form': mission_form,
        'vision_form': vision_form,
        'values_section_form': values_section_form,
        'timeline_section_form': timeline_section_form,
        'values': values,
        'timeline_items': timeline_items,
        'has_perm': request.user.is_staff,
    }
    
    return render(request, 'admin/about_settings.html', context)

