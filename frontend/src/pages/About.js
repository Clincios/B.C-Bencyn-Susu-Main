import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { axiosInstance } from '../config/api';
import { API_ENDPOINTS } from '../config/api';
import PageErrorBoundary from '../components/PageErrorBoundary';
import './About.css';

const About = () => {
  const [aboutData, setAboutData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [storyImage, setStoryImage] = useState(null);

  useEffect(() => {
    fetchAboutPage();
    fetchStoryImage();
  }, []);

  const fetchAboutPage = async () => {
    try {
      // Fetch all sections independently
      const [storyRes, missionRes, visionRes, valuesHeaderRes, timelineHeaderRes, valuesRes, timelineRes] = await Promise.all([
        axiosInstance.get(API_ENDPOINTS.ABOUT_STORY),
        axiosInstance.get(API_ENDPOINTS.ABOUT_MISSION),
        axiosInstance.get(API_ENDPOINTS.ABOUT_VISION),
        axiosInstance.get(API_ENDPOINTS.ABOUT_VALUES_HEADER),
        axiosInstance.get(API_ENDPOINTS.ABOUT_TIMELINE_HEADER),
        axiosInstance.get(API_ENDPOINTS.ABOUT_VALUES),
        axiosInstance.get(API_ENDPOINTS.ABOUT_TIMELINE_ITEMS)
      ]);

      // Handle paginated responses
      const storyData = storyRes.data.results || storyRes.data;
      const missionData = missionRes.data.results || missionRes.data;
      const visionData = visionRes.data.results || visionRes.data;
      const valuesHeaderData = valuesHeaderRes.data.results || valuesHeaderRes.data;
      const timelineHeaderData = timelineHeaderRes.data.results || timelineHeaderRes.data;
      const valuesData = valuesRes.data.results || valuesRes.data;
      const timelineData = timelineRes.data.results || timelineRes.data;

      // Combine all data
      setAboutData({
        story_title: Array.isArray(storyData) && storyData.length > 0 ? storyData[0].title : null,
        story_content: Array.isArray(storyData) && storyData.length > 0 ? storyData[0].content : null,
        mission_title: Array.isArray(missionData) && missionData.length > 0 ? missionData[0].title : null,
        mission_content: Array.isArray(missionData) && missionData.length > 0 ? missionData[0].content : null,
        vision_title: Array.isArray(visionData) && visionData.length > 0 ? visionData[0].title : null,
        vision_content: Array.isArray(visionData) && visionData.length > 0 ? visionData[0].content : null,
        values_title: Array.isArray(valuesHeaderData) && valuesHeaderData.length > 0 ? valuesHeaderData[0].title : null,
        values_subtitle: Array.isArray(valuesHeaderData) && valuesHeaderData.length > 0 ? valuesHeaderData[0].subtitle : null,
        timeline_title: Array.isArray(timelineHeaderData) && timelineHeaderData.length > 0 ? timelineHeaderData[0].title : null,
        timeline_subtitle: Array.isArray(timelineHeaderData) && timelineHeaderData.length > 0 ? timelineHeaderData[0].subtitle : null,
        values: Array.isArray(valuesData) ? valuesData : [],
        timeline_items: Array.isArray(timelineData) ? timelineData : []
      });
    } catch (error) {
      // Fallback to legacy endpoint if new endpoints fail
      try {
        const response = await axiosInstance.get(API_ENDPOINTS.ABOUT_PAGE);
        const dataArray = response.data.results || response.data;
        if (Array.isArray(dataArray) && dataArray.length > 0) {
          setAboutData(dataArray[0]);
        }
      } catch (legacyError) {
        // Legacy endpoint also failed, will use default data
      }
    } finally {
      setIsLoading(false);
    }
  };

  const fetchStoryImage = async () => {
    try {
      const response = await axiosInstance.get(`${API_ENDPOINTS.PAGE_IMAGES}?page=about&section=story`);
      const dataArray = response.data.results || response.data;
      if (Array.isArray(dataArray) && dataArray.length > 0) {
        setStoryImage(dataArray[0]);
      }
    } catch (error) {
      // Silently fall back to default card if story image not found
      // Error is intentionally ignored
    }
  };

  // Fallback data if API fails or no data
  const defaultValues = [
    {
      icon: '🎯',
      title: 'Integrity',
      description: 'We operate with the highest standards of honesty and transparency in all our dealings.'
    },
    {
      icon: '🤝',
      title: 'Trust',
      description: 'Building lasting relationships based on reliability and mutual respect.'
    },
    {
      icon: '💪',
      title: 'Excellence',
      description: 'Committed to delivering exceptional service and exceeding expectations.'
    },
    {
      icon: '🌱',
      title: 'Growth',
      description: 'Empowering our clients to achieve their financial goals and build wealth.'
    }
  ];

  const defaultTimeline = [
    {
      year: '2014',
      title: 'Foundation',
      description: 'B.C BENCYN SUSU was established with a vision to provide accessible financial services.'
    },
    {
      year: '2017',
      title: 'Expansion',
      description: 'Expanded our services to reach more communities across the region.'
    },
    {
      year: '2020',
      title: 'Digital Transformation',
      description: 'Launched digital platforms to enhance customer experience and accessibility.'
    },
    {
      year: '2024',
      title: 'Innovation',
      description: 'Continuing to innovate and serve thousands of satisfied customers.'
    }
  ];

  const values = aboutData?.values || defaultValues;
  const timeline = aboutData?.timeline_items || defaultTimeline;

  if (isLoading) {
    return (
      <PageErrorBoundary>
        <div className="about">
          <div style={{ 
            minHeight: '60vh', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center' 
          }}>
            <div className="spinner" style={{
              width: '48px',
              height: '48px',
              border: '4px solid #f3f4f6',
              borderTopColor: '#FF8C00',
              borderRadius: '50%',
              animation: 'spin 1s linear infinite'
            }}></div>
          </div>
        </div>
      </PageErrorBoundary>
    );
  }

  return (
    <PageErrorBoundary>
      <div className="about">
      <section className="about-hero">
        <div className="container">
          <motion.div
            className="about-hero-content"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="about-title">About <span className="about-title-brand">B.C BENCYN SUSU</span></h1>
            <p className="about-subtitle">
              Building financial security and prosperity for individuals and communities 
              through trusted susu collection services.
            </p>
          </motion.div>
        </div>
      </section>

      <section className="about-story section">
        <div className="container">
          <div className="story-content">
            <motion.div
              className="story-text"
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
            >
              <h2 className="story-title">{aboutData?.story_title || 'Our Story'}</h2>
              {aboutData?.story_content ? (
                <div className="story-paragraph" style={{ whiteSpace: 'pre-line' }}>
                  {aboutData.story_content}
                </div>
              ) : (
                <>
                  <p className="story-paragraph">
                    B.C BENCYN SUSU was founded with a simple yet powerful mission: to make 
                    financial services accessible to everyone. We recognized the need for 
                    reliable, transparent susu collection services that honor traditional 
                    values while embracing modern financial practices.
                  </p>
                  <p className="story-paragraph">
                    Over the years, we have grown from a small community-focused organization 
                    to a trusted financial partner serving thousands of clients. Our commitment 
                    to integrity, transparency, and customer satisfaction has been the cornerstone 
                    of our success.
                  </p>
                  <p className="story-paragraph">
                    Today, we continue to innovate and expand our services, always keeping our 
                    clients' financial well-being at the heart of everything we do.
                  </p>
                </>
              )}
            </motion.div>
            <motion.div
              className="story-image"
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
            >
              {storyImage && storyImage.image_url ? (
                <div className="story-card-image">
                  <img 
                    src={storyImage.image_url} 
                    alt={storyImage.title || 'About Story Image'}
                    className="story-img"
                  />
                </div>
              ) : (
                <div className="story-card">
                  <div className="story-card-content">
                    <div className="story-icon">💼</div>
                    <h3>Trusted Financial Partner</h3>
                    <p>Over 10 years of dedicated service</p>
                  </div>
                </div>
              )}
            </motion.div>
          </div>
        </div>
      </section>

      <section className="values-section section">
        <div className="container">
          <h2 className="section-title">{aboutData?.values_title || 'Our Core Values'}</h2>
          {aboutData?.values_subtitle && (
            <p className="section-subtitle">
              {aboutData.values_subtitle}
            </p>
          )}
          {!aboutData?.values_subtitle && (
            <p className="section-subtitle">
              The principles that guide everything we do at B.C BENCYN SUSU.
            </p>
          )}
          <div className="values-grid">
            {values.map((value, index) => (
              <motion.div
                key={index}
                className="value-card"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                whileHover={{ y: -5 }}
              >
                <div className="value-icon">{value.icon}</div>
                <h3 className="value-title">{value.title}</h3>
                <p className="value-description">{value.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="timeline-section section">
        <div className="container">
          <h2 className="section-title">{aboutData?.timeline_title || 'Our Journey'}</h2>
          {aboutData?.timeline_subtitle && (
            <p className="section-subtitle">
              {aboutData.timeline_subtitle}
            </p>
          )}
          {!aboutData?.timeline_subtitle && (
            <p className="section-subtitle">
              Key milestones in our growth and development.
            </p>
          )}
          <div className="timeline">
            {timeline.map((item, index) => (
              <motion.div
                key={index}
                className="timeline-item"
                initial={{ opacity: 0, x: index % 2 === 0 ? -30 : 30 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <div className="timeline-marker"></div>
                <div className="timeline-content">
                  <div className="timeline-year">{item.year}</div>
                  <h3 className="timeline-title">{item.title}</h3>
                  <p className="timeline-description">{item.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="mission-section section">
        <div className="container">
          <div className="mission-content">
            <motion.div
              className="mission-card"
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
            >
              <h2 className="mission-title">{aboutData?.mission_title || 'Our Mission'}</h2>
              <p className="mission-text">
                {aboutData?.mission_content || 'To provide accessible, reliable, and transparent financial services that empower individuals and communities to achieve their financial goals and build lasting wealth through trusted susu collection practices.'}
              </p>
            </motion.div>
            <motion.div
              className="mission-card"
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <h2 className="mission-title">{aboutData?.vision_title || 'Our Vision'}</h2>
              <p className="mission-text">
                {aboutData?.vision_content || 'To become the leading susu financial institution, recognized for our integrity, innovation, and commitment to transforming lives through accessible financial services across the region.'}
              </p>
            </motion.div>
          </div>
        </div>
      </section>
      </div>
    </PageErrorBoundary>
  );
};

export default About;
