import React, { Component } from 'react';
import { Link } from 'react-router-dom';

/**
 * ErrorBoundary component catches JavaScript errors in child components
 * and displays a fallback UI instead of crashing the app.
 */
class ErrorBoundary extends Component {
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
      console.error('ErrorBoundary caught an error:', error, errorInfo);
    }
    // In production, you might want to send this to an error tracking service
    // e.g., Sentry, LogRocket, etc.
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <div className="error-boundary-content">
            <div className="error-icon">⚠️</div>
            <h1>Something went wrong</h1>
            <p>We're sorry, but something unexpected happened. Please try again.</p>
            <div className="error-actions">
              <button onClick={this.handleRetry} className="btn btn-primary">
                Try Again
              </button>
              <Link to="/" className="btn btn-secondary">
                Go Home
              </Link>
            </div>
          </div>
          <style>{`
            .error-boundary {
              min-height: 100vh;
              display: flex;
              align-items: center;
              justify-content: center;
              padding: 2rem;
              background: linear-gradient(135deg, #F9FAFB 0%, #FFFFFF 100%);
            }
            .error-boundary-content {
              text-align: center;
              max-width: 400px;
            }
            .error-icon {
              font-size: 4rem;
              margin-bottom: 1rem;
            }
            .error-boundary h1 {
              font-size: 1.75rem;
              color: #111827;
              margin-bottom: 0.75rem;
            }
            .error-boundary p {
              color: #6B7280;
              margin-bottom: 1.5rem;
              line-height: 1.6;
            }
            .error-actions {
              display: flex;
              gap: 1rem;
              justify-content: center;
              flex-wrap: wrap;
            }
            .error-actions .btn {
              padding: 0.75rem 1.5rem;
              border-radius: 0.5rem;
              font-weight: 600;
              text-decoration: none;
              cursor: pointer;
              border: 2px solid transparent;
              transition: all 0.3s ease;
            }
            .error-actions .btn-primary {
              background: linear-gradient(135deg, #FF8C00, #E67A00);
              color: white;
            }
            .error-actions .btn-secondary {
              background: white;
              color: #FF8C00;
              border-color: #FF8C00;
            }
          `}</style>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
