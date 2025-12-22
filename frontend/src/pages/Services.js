import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { axiosInstance } from '../config/api';
import { API_ENDPOINTS } from '../config/api';
import PageErrorBoundary from '../components/PageErrorBoundary';
import './Services.css';

const Services = () => {
  const [services, setServices] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [headerImage, setHeaderImage] = useState(null);

  const fetchServices = useCallback(async () => {
    try {
      const response = await axiosInstance.get(API_ENDPOINTS.SERVICES);
      // Handle paginated response from Django REST Framework
      const dataArray = response.data.results || response.data;
      
      if (dataArray && Array.isArray(dataArray) && dataArray.length > 0) {
        // Map API service types to colors
        const serviceColorMap = {
          'susu': 'orange',
          'savings': 'green',
          'advisory': 'orange',
          'loans': 'green',
          'group': 'orange',
          'digital': 'green'
        };
        
        // Map service types to default features
        const defaultFeaturesMap = {
          'susu': [
            'Flexible payment schedules',
            'Secure collection process',
            'Transparent record keeping',
            'Multiple contribution options'
          ],
          'savings': [
            'Goal-oriented savings',
            'Competitive interest rates',
            'Flexible withdrawal options',
            'Personalized plans'
          ],
          'advisory': [
            'Personalized consultations',
            'Investment guidance',
            'Budget planning',
            'Financial education'
          ],
          'loans': [
            'Quick approval process',
            'Flexible repayment terms',
            'Competitive interest rates',
            'No hidden fees'
          ],
          'group': [
            'Group management tools',
            'Automated collections',
            'Transparent reporting',
            'Dedicated support'
          ],
          'digital': [
            '24/7 account access',
            'Mobile app available',
            'Secure transactions',
            'Real-time updates'
          ]
        };
        
        const mappedServices = dataArray.map(service => ({
          ...service,
          color: serviceColorMap[service.service_type] || 'orange',
          features: defaultFeaturesMap[service.service_type] || [] // Add default features based on service type
        }));
        setServices(mappedServices);
      } else {
        // If no services from API, use default services
        setServices(getDefaultServices());
      }
    } catch (error) {
      // Fallback to default services
      setServices(getDefaultServices());
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchHeaderImage = useCallback(async () => {
    try {
      const response = await axiosInstance.get(`${API_ENDPOINTS.PAGE_IMAGES}?page=services&section=header`);
      const dataArray = response.data.results || response.data;
      if (Array.isArray(dataArray) && dataArray.length > 0) {
        setHeaderImage(dataArray[0]);
      }
    } catch (error) {
      // Silently fall back to default if header image not found
      // Error is intentionally ignored
    }
  }, []);

  useEffect(() => {
    fetchServices();
    fetchHeaderImage();
  }, [fetchServices, fetchHeaderImage]);

  const getDefaultServices = () => [
    {
      icon: '💵',
      title: 'Susu Collection',
      description: 'Regular collection services with flexible payment schedules. Choose from daily, weekly, or monthly contributions.',
      features: [
        'Flexible payment schedules',
        'Secure collection process',
        'Transparent record keeping',
        'Multiple contribution options'
      ],
      color: 'orange'
    },
    {
      icon: '💰',
      title: 'Savings Plans',
      description: 'Structured savings plans designed to help you achieve your financial goals with competitive returns.',
      features: [
        'Goal-oriented savings',
        'Competitive interest rates',
        'Flexible withdrawal options',
        'Personalized plans'
      ],
      color: 'green'
    },
    {
      icon: '📊',
      title: 'Financial Advisory',
      description: 'Expert financial advice to help you make informed decisions about your money and investments.',
      features: [
        'Personalized consultations',
        'Investment guidance',
        'Budget planning',
        'Financial education'
      ],
      color: 'orange'
    },
    {
      icon: '🏦',
      title: 'Loan Services',
      description: 'Accessible loan services with flexible repayment terms to meet your immediate financial needs.',
      features: [
        'Quick approval process',
        'Flexible repayment terms',
        'Competitive interest rates',
        'No hidden fees'
      ],
      color: 'green'
    },
    {
      icon: '👥',
      title: 'Group Susu',
      description: 'Organize group susu schemes for your community, workplace, or organization with our support.',
      features: [
        'Group management tools',
        'Automated collections',
        'Transparent reporting',
        'Dedicated support'
      ],
      color: 'orange'
    },
    {
      icon: '📱',
      title: 'Digital Services',
      description: 'Manage your susu account online with our secure digital platform. Access your account anytime, anywhere.',
      features: [
        '24/7 account access',
        'Mobile app available',
        'Secure transactions',
        'Real-time updates'
      ],
      color: 'green'
    }
  ];

  // Always show services - use API services if available, otherwise show defaults
  const displayServices = services.length > 0 ? services : getDefaultServices();

  return (
    <PageErrorBoundary>
      <div className="services">
      <section className="services-hero" style={headerImage && headerImage.image_url ? {
        backgroundImage: `linear-gradient(135deg, rgba(31, 41, 55, 0.85), rgba(17, 24, 39, 0.85)), url(${headerImage.image_url})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat'
      } : {}}>
        <div className="container">
          <motion.div
            className="services-hero-content"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="services-title">Our <span className="services-title-brand">Services</span></h1>
            <p className="services-subtitle">
              Comprehensive financial solutions tailored to meet your needs. 
              From traditional susu collection to modern digital services.
            </p>
          </motion.div>
        </div>
      </section>

      <section className="services-list section">
        <div className="container">
          {isLoading ? (
            <div style={{ textAlign: 'center', padding: 'var(--spacing-3xl) 0' }}>
              <div className="spinner"></div>
              <p>Loading services...</p>
            </div>
          ) : (
            <div className="services-grid">
              {displayServices.map((service, index) => (
              <motion.div
                key={index}
                className={`service-card service-card-${service.color}`}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                whileHover={{ y: -10 }}
              >
                <div className="service-icon">{service.icon || '💰'}</div>
                <h3 className="service-title">{service.title}</h3>
                <p className="service-description">{service.description}</p>
                {service.features && service.features.length > 0 && (
                  <ul className="service-features">
                    {service.features.map((feature, idx) => (
                      <li key={idx}>
                        <span className="feature-check">✓</span>
                        {feature}
                      </li>
                    ))}
                  </ul>
                )}
                <Link to="/contact" className="service-cta">
                  Learn More
                </Link>
              </motion.div>
              ))}
            </div>
          )}
        </div>
      </section>

      <section className="services-cta section">
        <div className="container">
          <motion.div
            className="services-cta-content"
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="services-cta-title">Ready to Get Started?</h2>
            <p className="services-cta-subtitle">
              Contact us today to learn more about our services and find the perfect 
              financial solution for your needs.
            </p>
            <Link to="/contact" className="btn btn-primary btn-large">
              Contact Us Now
            </Link>
          </motion.div>
        </div>
      </section>
      </div>
    </PageErrorBoundary>
  );
};

export default Services;
