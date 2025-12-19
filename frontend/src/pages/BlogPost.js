import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { axiosInstance } from '../config/api';
import { API_ENDPOINTS } from '../config/api';
import { format } from 'date-fns';
import PageErrorBoundary from '../components/PageErrorBoundary';
import { Calendar, User, ArrowRight } from '../components/ui/Icon';
import { FaFacebook, FaTwitter, FaLinkedin, FaWhatsapp } from 'react-icons/fa';
import './BlogPost.css';

export default function BlogPost() {
  const { id } = useParams();
  const [post, setPost] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);

  useEffect(() => {
    fetchPost();
  }, [id]);

  const fetchPost = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await axiosInstance.get(`${API_ENDPOINTS.BLOG_POSTS}${id}/`);
      setPost(response.data);
    } catch (error) {
      setError('Post not found');
    } finally {
      setIsLoading(false);
    }
  };

  // Lightbox handlers
  const openLightbox = (image) => {
    setSelectedImage(image);
    document.body.style.overflow = 'hidden';
  };

  const closeLightbox = () => {
    setSelectedImage(null);
    document.body.style.overflow = '';
  };

  // Close lightbox on escape key
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        closeLightbox();
      }
    };
    if (selectedImage) {
      document.addEventListener('keydown', handleEscape);
    }
    return () => document.removeEventListener('keydown', handleEscape);
  }, [selectedImage]);

  if (isLoading) {
    return (
      <div className="blog-post-page">
        <div className="container">
          <div className="blog-post-loading">
            <div className="spinner"></div>
            <p>Loading article...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="blog-post-page">
        <div className="container">
          <div className="blog-post-error">
            <h2>Post Not Found</h2>
            <p>The article you're looking for doesn't exist.</p>
            <Link to="/blog" className="btn btn-primary">
              Back to Blog
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const hasImages = post.images && post.images.length > 0;
  const hasVideos = post.videos && post.videos.length > 0;
  const hasMedia = hasImages || hasVideos;

  return (
    <PageErrorBoundary>
      <div className="blog-post-page">
        {isLoading ? (
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
        ) : error ? (
          <div style={{ 
            minHeight: '60vh', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            textAlign: 'center'
          }}>
            <div>
              <h2>{error}</h2>
              <Link to="/blog" style={{ marginTop: '1rem', display: 'inline-block' }}>
                Back to Blog
              </Link>
            </div>
          </div>
        ) : (
          <>
          <article className="blog-post-article">
        {post.featured_image_url && (
          <div className="blog-post-hero-image">
            <img src={post.featured_image_url} alt={post.title} />
          </div>
        )}
        
        <div className="container">
          <div className="blog-post-header">
            <Link to="/blog" className="blog-post-back">
              <ArrowRight size={16} style={{ transform: 'rotate(180deg)' }} />
              Back to Blog
            </Link>
            
            <div className="blog-post-meta-top">
              <span className={`blog-post-category blog-post-category-${post.category.toLowerCase().replace(' ', '-')}`}>
                {post.category}
              </span>
              <div className="blog-post-date-author">
                {post.author && (
                  <div className="blog-post-meta-item">
                    <User size={16} />
                    <span>{post.author}</span>
                  </div>
                )}
                <div className="blog-post-meta-item">
                  <Calendar size={16} />
                  <span>{format(new Date(post.created_date), 'MMMM d, yyyy')}</span>
                </div>
              </div>
            </div>
            
            <h1 className="blog-post-title">{post.title}</h1>
            
            {post.excerpt && (
              <p className="blog-post-excerpt">{post.excerpt}</p>
            )}
          </div>

          <div className="blog-post-content">
            <div 
              className="blog-post-body"
              dangerouslySetInnerHTML={{ __html: post.content.replace(/\n/g, '<br />') }}
            />

            {/* Videos Section */}
            {hasVideos && (
              <motion.section 
                className="blog-post-media-section"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                <h3 className="media-section-title">
                  <span className="media-icon">🎬</span>
                  Videos
                </h3>
                <div className="blog-videos-grid">
                  {post.videos.map((video, index) => (
                    <motion.div 
                      key={video.id || index}
                      className="blog-video-item"
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 0.1 * index }}
                    >
                      {video.video_type === 'upload' && video.video_file_url ? (
                        <div className="video-player-wrapper">
                          <video 
                            controls 
                            poster={video.thumbnail_url}
                            preload="metadata"
                            className="video-player"
                          >
                            <source src={video.video_file_url} type="video/mp4" />
                            Your browser does not support the video tag.
                          </video>
                        </div>
                      ) : video.embed_url ? (
                        <div className="video-embed-wrapper">
                          <iframe
                            src={video.embed_url}
                            title={video.title || `Video ${index + 1}`}
                            frameBorder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowFullScreen
                            className="video-embed"
                          />
                        </div>
                      ) : null}
                      {video.title && (
                        <p className="video-title">{video.title}</p>
                      )}
                    </motion.div>
                  ))}
                </div>
              </motion.section>
            )}

            {/* Images Gallery Section */}
            {hasImages && (
              <motion.section 
                className="blog-post-media-section"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
              >
                <h3 className="media-section-title">
                  <span className="media-icon">📷</span>
                  Photo Gallery
                </h3>
                <div className="blog-images-grid">
                  {post.images.map((image, index) => (
                    <motion.figure 
                      key={image.id || index}
                      className="blog-image-item"
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 0.1 * index }}
                      onClick={() => openLightbox(image)}
                      tabIndex={0}
                      onKeyDown={(e) => e.key === 'Enter' && openLightbox(image)}
                      role="button"
                      aria-label={`View ${image.alt_text || image.caption || 'image'} in full size`}
                    >
                      <div className="image-wrapper">
                        <img 
                          src={image.image_url} 
                          alt={image.alt_text || image.caption || `Image ${index + 1}`}
                          loading="lazy"
                        />
                        <div className="image-overlay">
                          <span className="zoom-icon">🔍</span>
                        </div>
                      </div>
                      {image.caption && (
                        <figcaption className="image-caption">{image.caption}</figcaption>
                      )}
                    </motion.figure>
                  ))}
                </div>
              </motion.section>
            )}
          </div>

          {/* Share and Navigation */}
          <div className="blog-post-footer">
            <div className="blog-post-share">
              <span className="share-label">Share this article:</span>
              <div className="share-buttons">
                <a 
                  href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(post.title)}&url=${encodeURIComponent(window.location.href)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="share-btn share-twitter"
                  aria-label="Share on Twitter"
                >
                  <FaTwitter className="share-icon" />
                </a>
                <a 
                  href={`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(window.location.href)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="share-btn share-facebook"
                  aria-label="Share on Facebook"
                >
                  <FaFacebook className="share-icon" />
                </a>
                <a 
                  href={`https://www.linkedin.com/shareArticle?mini=true&url=${encodeURIComponent(window.location.href)}&title=${encodeURIComponent(post.title)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="share-btn share-linkedin"
                  aria-label="Share on LinkedIn"
                >
                  <FaLinkedin className="share-icon" />
                </a>
                <a 
                  href={`https://wa.me/?text=${encodeURIComponent(post.title + ' ' + window.location.href)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="share-btn share-whatsapp"
                  aria-label="Share on WhatsApp"
                >
                  <FaWhatsapp className="share-icon" />
                </a>
              </div>
            </div>
            <Link to="/blog" className="btn btn-primary">
              ← Back to All Articles
            </Link>
          </div>
        </div>
      </article>

      {/* Image Lightbox Modal */}
      {selectedImage && (
        <div 
          className="lightbox-overlay" 
          onClick={closeLightbox}
          role="dialog"
          aria-modal="true"
          aria-label="Image lightbox"
        >
          <button 
            className="lightbox-close" 
            onClick={closeLightbox}
            aria-label="Close lightbox"
          >
            ✕
          </button>
          <div className="lightbox-content" onClick={(e) => e.stopPropagation()}>
            <img 
              src={selectedImage.image_url} 
              alt={selectedImage.alt_text || selectedImage.caption || 'Full size image'}
            />
            {selectedImage.caption && (
              <p className="lightbox-caption">{selectedImage.caption}</p>
            )}
          </div>
        </div>
      )}
          </>
        )}
      </div>
    </PageErrorBoundary>
  );
}
