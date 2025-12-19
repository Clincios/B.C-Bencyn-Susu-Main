import React, { Component } from 'react';
import { Link } from 'react-router-dom';

/**
 * PageErrorBoundary component for individual pages
 * Provides page-specific error handling with better UX
 */
class PageErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // Log error to console in development only
    if (process.env.NODE_ENV === 'development') {
      console.error('PageErrorBoundary caught an error:', error, errorInfo);
    }
    // In production, you might want to send this to an error tracking service
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null });
    // Try to reload just the component by resetting state
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="page-error-boundary" style={{
          minHeight: '60vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '2rem',
          textAlign: 'center'
        }}>
          <div className="page-error-content" style={{
            maxWidth: '500px'
          }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>⚠️</div>
            <h2 style={{ 
              fontSize: '1.5rem', 
              color: '#111827', 
              marginBottom: '0.75rem' 
            }}>
              Oops! Something went wrong
            </h2>
            <p style={{ 
              color: '#6B7280', 
              marginBottom: '1.5rem',
              lineHeight: '1.6'
            }}>
              We encountered an error while loading this page. Please try again.
            </p>
            <div style={{
              display: 'flex',
              gap: '1rem',
              justifyContent: 'center',
              flexWrap: 'wrap'
            }}>
              <button 
                onClick={this.handleRetry} 
                style={{
                  padding: '0.75rem 1.5rem',
                  borderRadius: '0.5rem',
                  fontWeight: '600',
                  cursor: 'pointer',
                  border: 'none',
                  background: 'linear-gradient(135deg, #FF8C00, #E67A00)',
                  color: 'white',
                  transition: 'all 0.3s ease'
                }}
              >
                Try Again
              </button>
              <Link 
                to="/" 
                style={{
                  padding: '0.75rem 1.5rem',
                  borderRadius: '0.5rem',
                  fontWeight: '600',
                  textDecoration: 'none',
                  background: 'white',
                  color: '#FF8C00',
                  border: '2px solid #FF8C00',
                  transition: 'all 0.3s ease',
                  display: 'inline-block'
                }}
              >
                Go Home
              </Link>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default PageErrorBoundary;

