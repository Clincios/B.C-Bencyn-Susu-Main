import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { axiosInstance } from '../config/api';
import { API_ENDPOINTS } from '../config/api';
import { FaFacebook, FaTwitter, FaInstagram, FaLinkedin } from 'react-icons/fa';
import './Footer.css';

const Footer = () => {
  const currentYear = new Date().getFullYear();
  const [contactInfo, setContactInfo] = useState(null);

  useEffect(() => {
    fetchContactInfo();
  }, []);

  const fetchContactInfo = async () => {
    try {
      const response = await axiosInstance.get(API_ENDPOINTS.CONTACT_INFORMATION);
      const dataArray = response.data.results || response.data;
      if (Array.isArray(dataArray) && dataArray.length > 0) {
        setContactInfo(dataArray[0]);
      }
    } catch (error) {
      // Silently fail - will show default info
      // Error is intentionally ignored
    }
  };

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  };

  // Get contact details from API or use defaults
  const address = contactInfo?.address_line1 || contactInfo?.address_line2 
    ? [contactInfo.address_line1, contactInfo.address_line2].filter(Boolean).join(', ')
    : 'Your Business Address, City, Country';
  
  const phone = contactInfo?.phone_primary || '+233 XX XXX XXXX';
  const email = contactInfo?.email_primary || 'info@bencynsusu.com';

  return (
    <footer className="footer" role="contentinfo">
      <div className="footer-container">
        <div className="footer-content">
          <div className="footer-section footer-brand">
            <Link to="/" className="footer-logo" onClick={scrollToTop} aria-label="B.C BENCYN SUSU Home">
              <span className="logo-text">B.C</span>
              <span className="logo-text-main">BENCYN</span>
              <span className="logo-text-sub">SUSU</span>
            </Link>
            <p className="footer-description">
              Your trusted financial partner for susu services. Building financial security, one contribution at a time.
            </p>
            <div className="footer-social" aria-label="Social media links">
              {contactInfo?.facebook_url && (
                <a href={contactInfo.facebook_url} target="_blank" rel="noopener noreferrer" aria-label="Facebook">
                  <FaFacebook className="social-icon" />
                </a>
              )}
              {contactInfo?.twitter_url && (
                <a href={contactInfo.twitter_url} target="_blank" rel="noopener noreferrer" aria-label="Twitter">
                  <FaTwitter className="social-icon" />
                </a>
              )}
              {contactInfo?.instagram_url && (
                <a href={contactInfo.instagram_url} target="_blank" rel="noopener noreferrer" aria-label="Instagram">
                  <FaInstagram className="social-icon" />
                </a>
              )}
              {contactInfo?.linkedin_url && (
                <a href={contactInfo.linkedin_url} target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
                  <FaLinkedin className="social-icon" />
                </a>
              )}
            </div>
          </div>

          <div className="footer-section">
            <h4 className="footer-title">Quick Links</h4>
            <nav aria-label="Footer navigation - Quick links">
              <ul className="footer-links">
                <li><Link to="/" onClick={scrollToTop}>Home</Link></li>
                <li><Link to="/about" onClick={scrollToTop}>About Us</Link></li>
                <li><Link to="/services" onClick={scrollToTop}>Services</Link></li>
                <li><Link to="/blog" onClick={scrollToTop}>Blog</Link></li>
                <li><Link to="/contact" onClick={scrollToTop}>Contact</Link></li>
              </ul>
            </nav>
          </div>

          <div className="footer-section">
            <h4 className="footer-title">Our Services</h4>
            <nav aria-label="Footer navigation - Services">
              <ul className="footer-links">
                <li><Link to="/services" onClick={scrollToTop}>Susu Collection</Link></li>
                <li><Link to="/services" onClick={scrollToTop}>Savings Plans</Link></li>
                <li><Link to="/services" onClick={scrollToTop}>Financial Advisory</Link></li>
                <li><Link to="/services" onClick={scrollToTop}>Loan Services</Link></li>
                <li><Link to="/services" onClick={scrollToTop}>Digital Services</Link></li>
              </ul>
            </nav>
          </div>

          <div className="footer-section">
            <h4 className="footer-title">Contact Info</h4>
            <address className="footer-contact">
              <div className="contact-item">
                <span className="contact-icon" aria-hidden="true">📍</span>
                <span>{address}</span>
              </div>
              <div className="contact-item">
                <span className="contact-icon" aria-hidden="true">📞</span>
                <a href={`tel:${phone.replace(/\s/g, '')}`}>{phone}</a>
              </div>
              <div className="contact-item">
                <span className="contact-icon" aria-hidden="true">✉️</span>
                <a href={`mailto:${email}`}>{email}</a>
              </div>
              {contactInfo?.hours_weekdays && (
                <div className="contact-item">
                  <span className="contact-icon" aria-hidden="true">🕒</span>
                  <span>{contactInfo.hours_weekdays}</span>
                </div>
              )}
            </address>
          </div>
        </div>

        <div className="footer-bottom">
          <p>&copy; {currentYear} B.C BENCYN SUSU. All rights reserved.</p>
          <div className="footer-bottom-links">
            <Link to="/contact" onClick={scrollToTop}>Privacy Policy</Link>
            <span className="separator">•</span>
            <Link to="/contact" onClick={scrollToTop}>Terms of Service</Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
