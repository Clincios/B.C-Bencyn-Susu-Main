import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { axiosInstance } from '../config/api';
import { API_ENDPOINTS } from '../config/api';
import PageErrorBoundary from '../components/PageErrorBoundary';
import './Home.css';

const Home = () => {
  const [heroImage, setHeroImage] = useState(null);
  const [testimonials, setTestimonials] = useState([]);

  useEffect(() => {
    // Fetch active hero image
    axiosInstance.get(API_ENDPOINTS.HERO_IMAGES)
      .then(response => {
        const data = response.data;
        // Handle paginated or direct array response
        let imagesArray = [];
        if (Array.isArray(data)) {
          imagesArray = data;
        } else if (data && Array.isArray(data.results)) {
          imagesArray = data.results;
        }
        
        if (imagesArray && imagesArray.length > 0) {
          setHeroImage(imagesArray[0]);
        }
      })
      .catch(() => {
        // Silently fall back to default gradient if hero image not found
      });

    // Fetch testimonials
    fetchTestimonials();
  }, []);

  const fetchTestimonials = async () => {
    try {
      const response = await axiosInstance.get(API_ENDPOINTS.TESTIMONIALS);
      const dataArray = response.data.results || response.data;
      if (Array.isArray(dataArray) && dataArray.length > 0) {
        setTestimonials(dataArray);
      }
    } catch (error) {
      // Error fetching testimonials - will show empty section
    }
  };

  const features = [
    {
      icon: '💰',
      title: 'Secure Savings',
      description: 'Safe and reliable susu collection services with transparent processes.'
    },
    {
      icon: '📈',
      title: 'Financial Growth',
      description: 'Build your financial future with our structured savings plans.'
    },
    {
      icon: '🤝',
      title: 'Trusted Partner',
      description: 'Years of experience serving our community with integrity.'
    },
    {
      icon: '⚡',
      title: 'Quick Access',
      description: 'Fast and easy access to your funds when you need them most.'
    }
  ];

  const stats = [
    { number: '10+', label: 'Years Experience' },
    { number: '5000+', label: 'Happy Clients' },
    { number: '₵50M+', label: 'Assets Managed' },
    { number: '98%', label: 'Satisfaction Rate' }
  ];

  return (
    <PageErrorBoundary>
      <div className="home">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-container">
          <motion.div
            className="hero-content"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="hero-title">
              Your Trusted Financial
              <span className="gradient-text"> Partner</span>
            </h1>
            <p className="hero-subtitle">
              B.C BENCYN SUSU provides secure, reliable susu collection services 
              to help you achieve your financial goals. Join thousands of satisfied 
              customers building wealth through our trusted platform.
            </p>
            <div className="hero-buttons">
              <Link to="/contact" className="btn btn-primary">
                Get Started
              </Link>
              <Link to="/services" className="btn btn-secondary">
                Learn More
              </Link>
            </div>
          </motion.div>
          <motion.div
            className="hero-image"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            {heroImage && heroImage.image_url ? (
              <div className="hero-card-image">
                <img 
                  src={heroImage.image_url} 
                  alt={heroImage.title || 'Hero Image'}
                  className="hero-img"
                />
              </div>
            ) : (
              <div className="hero-card">
                <div className="card-glow"></div>
              </div>
            )}
          </motion.div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section">
        <div className="container">
          <div className="stats-grid">
            {stats.map((stat, index) => (
              <motion.div
                key={index}
                className="stat-card"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <div className="stat-number">{stat.number}</div>
                <div className="stat-label">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section section">
        <div className="container">
          <h2 className="section-title">Why Choose B.C BENCYN SUSU?</h2>
          <p className="section-subtitle">
            We combine traditional susu values with modern financial practices 
            to deliver exceptional service.
          </p>
          <div className="features-grid">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                className="feature-card"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                whileHover={{ y: -5 }}
              >
                <div className="feature-icon">{feature.icon}</div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      {testimonials.length > 0 && (
        <section className="testimonials-section section">
          <div className="container">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
            >
              <h2 className="section-title">What Our Clients Say</h2>
              <p className="section-subtitle">
                Don't just take our word for it. Here's what our satisfied customers have to say about us.
              </p>
              <div className="testimonials-grid">
                {testimonials.map((testimonial, index) => (
                  <motion.div
                    key={testimonial.id || index}
                    className="testimonial-card"
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5, delay: index * 0.1 }}
                    whileHover={{ y: -5 }}
                  >
                    <div className="testimonial-rating">
                      {[...Array(testimonial.rating || 5)].map((_, i) => (
                        <span key={i} className="star">⭐</span>
                      ))}
                    </div>
                    <p className="testimonial-message">"{testimonial.message}"</p>
                    <div className="testimonial-author">
                      <h4 className="testimonial-name">{testimonial.name}</h4>
                      {testimonial.role && (
                        <p className="testimonial-role">{testimonial.role}</p>
                      )}
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </div>
        </section>
      )}

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <motion.div
            className="cta-content"
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="cta-title">Ready to Start Your Savings Journey?</h2>
            <p className="cta-subtitle">
              Join thousands of satisfied members and take control of your financial future today
            </p>
            <Link to="/contact" className="btn btn-cta btn-large">
              Contact Us Now
              <span className="btn-arrow">→</span>
            </Link>
          </motion.div>
        </div>
      </section>
      </div>
    </PageErrorBoundary>
  );
};

export default Home;
