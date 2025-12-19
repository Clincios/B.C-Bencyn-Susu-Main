import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { axiosInstance } from '../config/api';
import { API_ENDPOINTS } from '../config/api';
import PageErrorBoundary from '../components/PageErrorBoundary';
import './Contact.css';

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: ''
  });
  const [formErrors, setFormErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);
  const [contactInfo, setContactInfo] = useState(null);
  const [isLoadingContact, setIsLoadingContact] = useState(true);

  useEffect(() => {
    fetchContactInformation();
  }, []);

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validateForm = () => {
    const errors = {};
    
    if (!formData.name.trim()) {
      errors.name = 'Name is required';
    }
    
    if (!formData.email.trim()) {
      errors.email = 'Email is required';
    } else if (!validateEmail(formData.email)) {
      errors.email = 'Please enter a valid email address';
    }
    
    if (!formData.subject.trim()) {
      errors.subject = 'Subject is required';
    }
    
    if (!formData.message.trim()) {
      errors.message = 'Message is required';
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
    // Clear error for this field when user starts typing
    if (formErrors[name]) {
      setFormErrors({
        ...formErrors,
        [name]: ''
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form before submission
    if (!validateForm()) {
      setSubmitStatus({ 
        type: 'error', 
        message: 'Please fix the errors in the form before submitting.' 
      });
      return;
    }
    
    setIsSubmitting(true);
    setSubmitStatus(null);

    try {
      const response = await axiosInstance.post(API_ENDPOINTS.CONTACT, formData);
      setSubmitStatus({ type: 'success', message: 'Thank you! Your message has been sent successfully.' });
      setFormData({
        name: '',
        email: '',
        phone: '',
        subject: '',
        message: ''
      });
      setFormErrors({});
    } catch (error) {
      if (error.code === 'ECONNABORTED') {
        setSubmitStatus({ 
          type: 'error', 
          message: 'Request timed out. Please check your connection and try again.' 
        });
      } else {
        setSubmitStatus({ 
          type: 'error', 
          message: 'Sorry, there was an error sending your message. Please try again or contact us directly.' 
        });
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const fetchContactInformation = async () => {
    try {
      const response = await axiosInstance.get(API_ENDPOINTS.CONTACT_INFORMATION);
      // Handle paginated response from Django REST Framework
      const dataArray = response.data.results || response.data;
      const data = Array.isArray(dataArray) && dataArray.length > 0 ? dataArray[0] : null;
      
      if (data) {
        const info = [];
        
        if (data.address_line1 || data.address_line2) {
          info.push({
            icon: '📍',
            title: 'Address',
            details: [data.address_line1, data.address_line2].filter(Boolean)
          });
        }
        
        if (data.phone_primary || data.phone_secondary) {
          info.push({
            icon: '📞',
            title: 'Phone',
            details: [data.phone_primary, data.phone_secondary].filter(Boolean)
          });
        }
        
        if (data.email_primary || data.email_secondary) {
          info.push({
            icon: '✉️',
            title: 'Email',
            details: [data.email_primary, data.email_secondary].filter(Boolean)
          });
        }
        
        if (data.hours_weekdays || data.hours_weekend) {
          info.push({
            icon: '🕒',
            title: 'Business Hours',
            details: [data.hours_weekdays, data.hours_weekend].filter(Boolean)
          });
        }
        
        setContactInfo(info.length > 0 ? info : getDefaultContactInfo());
      } else {
        setContactInfo(getDefaultContactInfo());
      }
    } catch (error) {
      setContactInfo(getDefaultContactInfo());
    } finally {
      setIsLoadingContact(false);
    }
  };

  const getDefaultContactInfo = () => [
    {
      icon: '📍',
      title: 'Address',
      details: ['Your Business Address', 'City, Country']
    },
    {
      icon: '📞',
      title: 'Phone',
      details: ['+233 XX XXX XXXX', '+233 XX XXX XXXX']
    },
    {
      icon: '✉️',
      title: 'Email',
      details: ['info@bencynsusu.com', 'support@bencynsusu.com']
    },
    {
      icon: '🕒',
      title: 'Business Hours',
      details: ['Monday - Friday: 8:00 AM - 6:00 PM', 'Saturday: 9:00 AM - 2:00 PM']
    }
  ];

  const displayContactInfo = contactInfo || getDefaultContactInfo();

  return (
    <PageErrorBoundary>
      <div className="contact">
      <section className="contact-hero">
        <div className="container">
          <motion.div
            className="contact-hero-content"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="contact-title">Get In <span className="contact-title-brand">Touch</span></h1>
            <p className="contact-subtitle">
              Have questions? We'd love to hear from you. Send us a message and 
              we'll respond as soon as possible.
            </p>
          </motion.div>
        </div>
      </section>

      <section className="contact-content section">
        <div className="container">
          <div className="contact-wrapper">
            <motion.div
              className="contact-info"
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
            >
              <h2 className="contact-info-title">Contact Information</h2>
              <p className="contact-info-subtitle">
                Reach out to us through any of these channels. We're here to help!
              </p>
              {isLoadingContact ? (
                <div style={{ textAlign: 'center', padding: 'var(--spacing-xl) 0' }}>
                  <div className="spinner"></div>
                  <p>Loading contact information...</p>
                </div>
              ) : (
                <div className="contact-info-grid">
                  {displayContactInfo.map((info, index) => (
                  <div key={index} className="contact-info-card">
                    <div className="contact-info-icon">{info.icon}</div>
                    <h3 className="contact-info-card-title">{info.title}</h3>
                    {info.details.map((detail, idx) => (
                      <p key={idx} className="contact-info-detail">{detail}</p>
                    ))}
                  </div>
                  ))}
                </div>
              )}
            </motion.div>

            <motion.div
              className="contact-form-wrapper"
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
            >
              <form className="contact-form" onSubmit={handleSubmit}>
                <div className="form-group">
                  <label htmlFor="name">Full Name *</label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    placeholder="Enter your full name"
                    className={formErrors.name ? 'error' : ''}
                  />
                  {formErrors.name && <span className="error-message">{formErrors.name}</span>}
                </div>

                <div className="form-group">
                  <label htmlFor="email">Email Address *</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    placeholder="Enter your email address"
                    className={formErrors.email ? 'error' : ''}
                  />
                  {formErrors.email && <span className="error-message">{formErrors.email}</span>}
                </div>

                <div className="form-group">
                  <label htmlFor="phone">Phone Number</label>
                  <input
                    type="tel"
                    id="phone"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    placeholder="Enter your phone number"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="subject">Subject *</label>
                  <input
                    type="text"
                    id="subject"
                    name="subject"
                    value={formData.subject}
                    onChange={handleChange}
                    required
                    placeholder="What is this regarding?"
                    className={formErrors.subject ? 'error' : ''}
                  />
                  {formErrors.subject && <span className="error-message">{formErrors.subject}</span>}
                </div>

                <div className="form-group">
                  <label htmlFor="message">Message *</label>
                  <textarea
                    id="message"
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    required
                    rows="6"
                    placeholder="Tell us how we can help you..."
                    className={formErrors.message ? 'error' : ''}
                  ></textarea>
                  {formErrors.message && <span className="error-message">{formErrors.message}</span>}
                </div>

                {submitStatus && (
                  <div className={`form-status ${submitStatus.type}`}>
                    {submitStatus.message}
                  </div>
                )}

                <button
                  type="submit"
                  className="form-submit"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? 'Sending...' : 'Send Message'}
                </button>
              </form>
            </motion.div>
          </div>
        </div>
      </section>
      </div>
    </PageErrorBoundary>
  );
};

export default Contact;
