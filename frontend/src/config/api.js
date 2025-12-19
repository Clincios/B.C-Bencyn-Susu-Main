/**
 * API Configuration for BENCYN SUSU Frontend
 * 
 * Environment Variables:
 * - REACT_APP_API_URL: Base URL for the API (default: http://localhost:8000)
 */

import axios from 'axios';

// API Base URL - uses environment variable in production
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Configure axios instance with timeout (30 seconds)
const axiosInstance = axios.create({
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Export configured axios instance
export { axiosInstance };

/**
 * API Endpoints
 * All endpoints are relative to the API_BASE_URL
 */
export const API_ENDPOINTS = {
  // Contact
  CONTACT: `${API_BASE_URL}/api/contact/`,
  CONTACT_INFORMATION: `${API_BASE_URL}/api/contact-information/`,
  
  // Services
  SERVICES: `${API_BASE_URL}/api/services/`,
  
  // Testimonials
  TESTIMONIALS: `${API_BASE_URL}/api/testimonials/`,
  
  // Images
  HERO_IMAGES: `${API_BASE_URL}/api/hero-images/`,
  PAGE_IMAGES: `${API_BASE_URL}/api/page-images/`,
  
  // Blog
  BLOG_POSTS: `${API_BASE_URL}/api/blog-posts/`,
  
  // Updates
  UPDATES: `${API_BASE_URL}/api/updates/`,
  
  // Gallery
  GALLERY: `${API_BASE_URL}/api/gallery/`,
  
  // About Page Sections
  ABOUT_PAGE: `${API_BASE_URL}/api/about-page/`, // Legacy endpoint
  ABOUT_STORY: `${API_BASE_URL}/api/about-story/`,
  ABOUT_MISSION: `${API_BASE_URL}/api/about-mission/`,
  ABOUT_VISION: `${API_BASE_URL}/api/about-vision/`,
  ABOUT_VALUES_HEADER: `${API_BASE_URL}/api/about-values-header/`,
  ABOUT_TIMELINE_HEADER: `${API_BASE_URL}/api/about-timeline-header/`,
  ABOUT_VALUES: `${API_BASE_URL}/api/about-values/`,
  ABOUT_TIMELINE_ITEMS: `${API_BASE_URL}/api/about-timeline-items/`,
};

/**
 * Helper function to handle API responses
 * Handles both paginated and non-paginated responses
 */
export const getDataArray = (response) => {
  const data = response.data;
  if (Array.isArray(data)) {
    return data;
  }
  if (data && Array.isArray(data.results)) {
    return data.results;
  }
  return [];
};

/**
 * Helper function to get first item from API response
 */
export const getFirstItem = (response) => {
  const dataArray = getDataArray(response);
  return dataArray.length > 0 ? dataArray[0] : null;
};

// Export both API_BASE_URL and axiosInstance
export { API_BASE_URL };
export default axiosInstance;
