import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { axiosInstance } from '../config/api';
import { API_ENDPOINTS } from '../config/api';
import { format } from 'date-fns';
import PageErrorBoundary from '../components/PageErrorBoundary';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';
import { Calendar } from '../components/ui/Icon';
import { Bell, AlertCircle, Newspaper, CalendarIcon } from '../components/ui/IconExtended';
import './Updates.css';

export default function Updates() {
  const [updates, setUpdates] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchUpdates();
  }, []);

  const fetchUpdates = async () => {
    setIsLoading(true);
    try {
      const response = await axiosInstance.get(API_ENDPOINTS.UPDATES);
      const data = response.data;
      let updatesArray = [];
      if (Array.isArray(data)) {
        updatesArray = data;
      } else if (data && Array.isArray(data.results)) {
        updatesArray = data.results;
      }
      setUpdates(updatesArray);
    } catch (error) {
      setUpdates([]);
    } finally {
      setIsLoading(false);
    }
  };

  const typeIcons = {
    announcement: Bell,
    alert: AlertCircle,
    news: Newspaper,
    event: CalendarIcon
  };

  const typeColors = {
    announcement: 'blue',
    alert: 'red',
    news: 'green',
    event: 'purple'
  };

  const priorityColors = {
    high: 'update-priority-high',
    medium: 'update-priority-medium',
    low: 'update-priority-low'
  };

  return (
    <PageErrorBoundary>
      <div className="updates-page">
      {/* Hero Section */}
      <section className="updates-hero">
        <div className="container">
          <motion.div
            className="updates-hero-content"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="updates-hero-title">Company <span className="updates-hero-title-brand">Updates</span></h1>
            <p className="updates-hero-subtitle">
              Stay informed with the latest news, announcements, and important information
            </p>
          </motion.div>
        </div>
      </section>

      {/* Updates List */}
      <section className="updates-list section">
        <div className="container">
          {isLoading ? (
            <div className="updates-loading">
              <div className="spinner"></div>
              <p>Loading updates...</p>
            </div>
          ) : updates.length === 0 ? (
            <Card className="updates-empty">
              <Bell size={48} />
              <h3 className="updates-empty-title">No updates yet</h3>
              <p className="updates-empty-text">Check back soon for the latest news and announcements</p>
            </Card>
          ) : (
            <div className="updates-container">
              {updates.map((update, index) => {
                const TypeIcon = typeIcons[update.type] || Bell;
                return (
                  <motion.div
                    key={update.id}
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5, delay: index * 0.1 }}
                  >
                    <Card
                      className={`update-card ${priorityColors[update.priority] || priorityColors.low}`}
                    >
                    <div className="update-card-content">
                      <div className={`update-icon-wrapper update-icon-${update.type}`}>
                        <TypeIcon size={24} />
                      </div>
                      <div className="update-main-content">
                        <div className="update-header">
                          <h3 className="update-title">
                            {update.title}
                          </h3>
                          <Badge variant={typeColors[update.type] || 'default'}>
                            {update.type}
                          </Badge>
                        </div>
                        <div className="update-body">
                          <p className="update-content">
                            {update.content}
                          </p>
                        </div>
                        <div className="update-footer">
                          <div className="update-meta">
                            <Calendar size={16} />
                            <span>{format(new Date(update.created_date), 'MMMM d, yyyy')}</span>
                          </div>
                          {update.priority === 'high' && (
                            <Badge variant="red" className="update-priority-badge">
                              High Priority
                            </Badge>
                          )}
                        </div>
                      </div>
                    </div>
                  </Card>
                  </motion.div>
                );
              })}
            </div>
          )}
        </div>
      </section>
      </div>
    </PageErrorBoundary>
  );
}
