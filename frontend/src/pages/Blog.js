import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { axiosInstance } from '../config/api';
import { API_ENDPOINTS } from '../config/api';
import { format } from 'date-fns';
import PageErrorBoundary from '../components/PageErrorBoundary';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';
import { Calendar, User, ArrowRight, Search } from '../components/ui/Icon';
import './Blog.css';

export default function Blog() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchPosts = useCallback(async () => {
    setIsLoading(true);
    try {
      const params = {};
      if (selectedCategory !== 'all') {
        params.category = selectedCategory;
      }
      if (searchTerm) {
        params.search = searchTerm;
      }
      
      const response = await axiosInstance.get(API_ENDPOINTS.BLOG_POSTS, { params });
      // Handle different response structures
      const data = response.data;
      // If it's paginated, get results array, otherwise use data directly
      let postsArray = [];
      if (Array.isArray(data)) {
        postsArray = data;
      } else if (data && Array.isArray(data.results)) {
        postsArray = data.results;
      } else if (data && typeof data === 'object') {
        // Fallback: try to extract array from response
        postsArray = [];
      }
      setPosts(postsArray);
    } catch (error) {
      setPosts([]);
    } finally {
      setIsLoading(false);
    }
  }, [selectedCategory, searchTerm]);

  useEffect(() => {
    fetchPosts();
  }, [fetchPosts]);

  const categories = ['all', 'Financial Tips', 'Company News', 'Savings Guide', 'Investment', 'Community'];

  const categoryColors = {
    'Financial Tips': 'blue',
    'Company News': 'purple',
    'Savings Guide': 'green',
    'Investment': 'amber',
    'Community': 'pink'
  };

  return (
    <PageErrorBoundary>
      <div className="blog-page">
      {/* Hero Section */}
      <section className="blog-hero">
        <div className="container">
          <motion.div
            className="blog-hero-content"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="blog-hero-title">Blog & <span className="blog-hero-title-brand">Insights</span></h1>
            <p className="blog-hero-subtitle">
              Expert advice, financial tips, and the latest news from B.C BENCYN SUSU
            </p>
          </motion.div>
        </div>
      </section>

      {/* Search and Filter */}
      <section className="blog-filters">
        <div className="container">
          <div className="blog-filters-content">
            <div className="blog-search-wrapper">
              <Search className="blog-search-icon" size={20} />
              <Input
                placeholder="Search articles..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="blog-search-input"
              />
            </div>
            <div className="blog-categories">
              {categories.map((category) => (
                <Button
                  key={category}
                  variant={selectedCategory === category ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setSelectedCategory(category)}
                >
                  {category === 'all' ? 'All' : category}
                </Button>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Blog Posts */}
      <section className="blog-posts section">
        <div className="container">
          {isLoading ? (
            <div className="blog-loading">
              <div className="spinner"></div>
              <p>Loading articles...</p>
            </div>
          ) : posts.length === 0 ? (
            <div className="blog-empty">
              <p>No articles found. Check back soon!</p>
            </div>
          ) : (
            <div className="blog-grid">
              {posts.map((post, index) => (
                <motion.div
                  key={post.id}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <Card className="blog-card">
                  {post.featured_image_url && (
                    <div className="blog-card-image">
                      <img
                        src={post.featured_image_url}
                        alt={post.title}
                        className="blog-card-img"
                      />
                    </div>
                  )}
                  <div className="blog-card-content">
                    <div className="blog-card-badge">
                      <Badge variant={categoryColors[post.category] || 'default'}>
                        {post.category}
                      </Badge>
                    </div>
                    <h3 className="blog-card-title">
                      {post.title}
                    </h3>
                    {post.excerpt && (
                      <p className="blog-card-excerpt">
                        {post.excerpt}
                      </p>
                    )}
                    <div className="blog-card-meta">
                      {post.author && (
                        <div className="blog-meta-item">
                          <User size={16} />
                          <span>{post.author}</span>
                        </div>
                      )}
                      <div className="blog-meta-item">
                        <Calendar size={16} />
                        <span>{format(new Date(post.created_date), 'MMM d, yyyy')}</span>
                      </div>
                    </div>
                    <Link to={`/blog/${post.id}`} className="blog-card-link">
                      <Button variant="ghost" className="blog-read-more">
                        Read More
                        <ArrowRight size={16} />
                      </Button>
                    </Link>
                  </div>
                </Card>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </section>
      </div>
    </PageErrorBoundary>
  );
}
