import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { axiosInstance } from '../config/api';
import { API_ENDPOINTS } from '../config/api';
import { format } from 'date-fns';
import PageErrorBoundary from '../components/PageErrorBoundary';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';
import { Calendar, Play, Image as ImageIcon } from '../components/ui/Icon';
import './Gallery.css';

// Component to generate thumbnail from uploaded video
const VideoThumbnail = ({ videoUrl, title, onThumbnailReady }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [thumbnailUrl, setThumbnailUrl] = useState(null);
  const [error, setError] = useState(false);
  const [isGenerating, setIsGenerating] = useState(true);

  useEffect(() => {
    if (!videoUrl || thumbnailUrl || error) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;

    if (!video || !canvas) return;

    const handleLoadedMetadata = () => {
      try {
        // Seek to first frame (0.1 seconds to ensure frame is loaded)
        video.currentTime = 0.1;
      } catch (e) {
        setError(true);
        setIsGenerating(false);
      }
    };

    const handleSeeked = () => {
      try {
        const ctx = canvas.getContext('2d');
        const width = video.videoWidth || 640;
        const height = video.videoHeight || 360;
        
        canvas.width = width;
        canvas.height = height;
        ctx.drawImage(video, 0, 0, width, height);
        
        const dataUrl = canvas.toDataURL('image/jpeg', 0.8);
        setThumbnailUrl(dataUrl);
        setIsGenerating(false);
        if (onThumbnailReady) {
          onThumbnailReady(dataUrl);
        }
      } catch (e) {
        setError(true);
        setIsGenerating(false);
      }
    };

    const handleError = () => {
      setError(true);
      setIsGenerating(false);
    };

    video.addEventListener('loadedmetadata', handleLoadedMetadata);
    video.addEventListener('seeked', handleSeeked);
    video.addEventListener('error', handleError);

    // Load the video
    video.load();

    return () => {
      video.removeEventListener('loadedmetadata', handleLoadedMetadata);
      video.removeEventListener('seeked', handleSeeked);
      video.removeEventListener('error', handleError);
    };
  }, [videoUrl, thumbnailUrl, error, onThumbnailReady]);

  return (
    <>
      <video
        ref={videoRef}
        src={videoUrl}
        preload="metadata"
        style={{ display: 'none' }}
        crossOrigin="anonymous"
        muted
      />
      <canvas ref={canvasRef} style={{ display: 'none' }} />
    </>
  );
};

// Helper function to get video thumbnail (with fallback handling)
const getVideoThumbnail = (item) => {
  // Backend now always provides thumbnail_url for YouTube/Vimeo videos
  // If it exists, use it; otherwise show placeholder
  return item.thumbnail_url || null;
};

export default function Gallery() {
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [mediaTypeFilter, setMediaTypeFilter] = useState('all');
  const [items, setItems] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedItem, setSelectedItem] = useState(null);
  const [videoThumbnails, setVideoThumbnails] = useState({});

  useEffect(() => {
    fetchGalleryItems();
  }, [selectedFilter, mediaTypeFilter]);

  const fetchGalleryItems = async () => {
    setIsLoading(true);
    try {
      const params = {};
      if (selectedFilter !== 'all') {
        params.event_type = selectedFilter;
      }
      if (mediaTypeFilter !== 'all') {
        params.media_type = mediaTypeFilter;
      }
      
      const response = await axiosInstance.get(API_ENDPOINTS.GALLERY, { params });
      const data = response.data;
      let itemsArray = [];
      
      if (Array.isArray(data)) {
        itemsArray = data;
      } else if (data && Array.isArray(data.results)) {
        itemsArray = data.results;
      }
      
      setItems(itemsArray);
    } catch (error) {
      setItems([]);
    } finally {
      setIsLoading(false);
    }
  };

  const eventTypes = [
    { value: 'all', label: 'All Events' },
    { value: 'meeting', label: 'Meetings' },
    { value: 'celebration', label: 'Celebrations' },
    { value: 'workshop', label: 'Workshops' },
    { value: 'community', label: 'Community' },
    { value: 'award', label: 'Awards' },
    { value: 'other', label: 'Other' },
  ];

  const openLightbox = (item) => {
    setSelectedItem(item);
    document.body.style.overflow = 'hidden';
  };

  const closeLightbox = () => {
    setSelectedItem(null);
    document.body.style.overflow = '';
  };

  // Close lightbox on escape key
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        closeLightbox();
      }
    };
    if (selectedItem) {
      document.addEventListener('keydown', handleEscape);
    }
    return () => document.removeEventListener('keydown', handleEscape);
  }, [selectedItem]);

  // Filter featured items
  const featuredItems = items.filter(item => item.is_featured);
  const regularItems = items.filter(item => !item.is_featured);

  return (
    <PageErrorBoundary>
      <div className="gallery-page">
      {/* Hero Section */}
      <section className="gallery-hero">
        <div className="container">
          <motion.div
            className="gallery-hero-content"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="gallery-hero-title">Event <span className="gallery-hero-title-brand">Gallery</span></h1>
            <p className="gallery-hero-subtitle">
              Explore our collection of images and videos from B.C BENCYN SUSU events and activities
            </p>
          </motion.div>
        </div>
      </section>

      {/* Filters */}
      <section className="gallery-filters">
        <div className="container">
          <div className="gallery-filters-content">
            <div className="gallery-filter-group">
              <label className="gallery-filter-label">Event Type:</label>
              <div className="gallery-filter-buttons">
                {eventTypes.map((type) => (
                  <Button
                    key={type.value}
                    variant={selectedFilter === type.value ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setSelectedFilter(type.value)}
                  >
                    {type.label}
                  </Button>
                ))}
              </div>
            </div>
            <div className="gallery-filter-group">
              <label className="gallery-filter-label">Media Type:</label>
              <div className="gallery-filter-buttons">
                <Button
                  variant={mediaTypeFilter === 'all' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setMediaTypeFilter('all')}
                >
                  All
                </Button>
                <Button
                  variant={mediaTypeFilter === 'image' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setMediaTypeFilter('image')}
                >
                  <ImageIcon size={16} style={{ marginRight: '4px' }} />
                  Images
                </Button>
                <Button
                  variant={mediaTypeFilter === 'video' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setMediaTypeFilter('video')}
                >
                  <Play size={16} style={{ marginRight: '4px' }} />
                  Videos
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Items */}
      {featuredItems.length > 0 && (
        <section className="gallery-featured section">
          <div className="container">
            <h2 className="gallery-section-title">Featured</h2>
            <div className="gallery-grid gallery-grid-featured">
              {featuredItems.map((item, index) => (
                <motion.div
                  key={item.id}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <Card className="gallery-card gallery-card-featured">
                    {item.media_type === 'image' && item.image_url && (
                      <div className="gallery-card-image" onClick={() => openLightbox(item)}>
                        <img src={item.image_url} alt={item.title} />
                        <div className="gallery-card-overlay">
                          <ImageIcon size={24} />
                        </div>
                      </div>
                    )}
                    {item.media_type === 'video' && (() => {
                      // Get thumbnail: custom > generated from URL > extracted from uploaded video > placeholder
                      let thumbnailUrl = getVideoThumbnail(item);
                      
                      // For uploaded videos without thumbnail, use extracted thumbnail if available
                      if (!thumbnailUrl && item.video_file_url && videoThumbnails[item.id]) {
                        thumbnailUrl = videoThumbnails[item.id];
                      }
                      
                      return (
                        <div className="gallery-card-video" onClick={() => openLightbox(item)}>
                          {thumbnailUrl ? (
                            <>
                              <img src={thumbnailUrl} alt={item.title} onError={(e) => {
                                // Fallback if thumbnail fails to load
                                e.target.style.display = 'none';
                                e.target.parentElement.innerHTML = '<div class="gallery-card-video-placeholder"><span style="font-size: 48px;">▶️</span><span>Video</span></div>';
                              }} />
                              <div className="gallery-card-overlay">
                                <Play size={32} />
                              </div>
                            </>
                          ) : item.video_file_url ? (
                            // For uploaded videos, generate thumbnail
                            <>
                              <VideoThumbnail
                                videoUrl={item.video_file_url}
                                title={item.title}
                                onThumbnailReady={(thumbUrl) => {
                                  setVideoThumbnails(prev => ({ ...prev, [item.id]: thumbUrl }));
                                }}
                              />
                              {videoThumbnails[item.id] ? (
                                <>
                                  <img src={videoThumbnails[item.id]} alt={item.title} />
                                  <div className="gallery-card-overlay">
                                    <Play size={32} />
                                  </div>
                                </>
                              ) : (
                                <div className="gallery-card-video-placeholder">
                                  <Play size={48} />
                                  <span>Loading...</span>
                                </div>
                              )}
                            </>
                          ) : (
                            <div className="gallery-card-video-placeholder">
                              <Play size={48} />
                              <span>Video</span>
                            </div>
                          )}
                        </div>
                      );
                    })()}
                    <div className="gallery-card-content">
                      <div className="gallery-card-badges">
                        <Badge variant="purple">
                          {eventTypes.find(t => t.value === item.event_type)?.label || item.event_type}
                        </Badge>
                        <Badge variant={item.media_type === 'image' ? 'blue' : 'red'}>
                          {item.media_type === 'image' ? 'Image' : 'Video'}
                        </Badge>
                      </div>
                      <h3 className="gallery-card-title">{item.title}</h3>
                      {item.description && (
                        <p className="gallery-card-description">{item.description}</p>
                      )}
                      {item.event_date && (
                        <div className="gallery-card-meta">
                          <Calendar size={16} />
                          <span>{format(new Date(item.event_date), 'MMM d, yyyy')}</span>
                        </div>
                      )}
                    </div>
                  </Card>
                </motion.div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Regular Items */}
      <section className="gallery-items section">
        <div className="container">
          {featuredItems.length > 0 && <h2 className="gallery-section-title">All Gallery Items</h2>}
          {isLoading ? (
            <div className="gallery-loading">
              <div className="spinner"></div>
              <p>Loading gallery...</p>
            </div>
          ) : regularItems.length === 0 && featuredItems.length === 0 ? (
            <div className="gallery-empty">
              <p>No gallery items found. Check back soon!</p>
            </div>
          ) : (
            <div className="gallery-grid">
              {regularItems.map((item, index) => (
                <motion.div
                  key={item.id}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.05 }}
                >
                  <Card className="gallery-card">
                    {item.media_type === 'image' && item.image_url && (
                      <div className="gallery-card-image" onClick={() => openLightbox(item)}>
                        <img src={item.image_url} alt={item.title} />
                        <div className="gallery-card-overlay">
                          <ImageIcon size={20} />
                        </div>
                      </div>
                    )}
                    {item.media_type === 'video' && (() => {
                      // Get thumbnail: custom > generated from URL > extracted from uploaded video > placeholder
                      let thumbnailUrl = getVideoThumbnail(item);
                      
                      // For uploaded videos without thumbnail, use extracted thumbnail if available
                      if (!thumbnailUrl && item.video_file_url && videoThumbnails[item.id]) {
                        thumbnailUrl = videoThumbnails[item.id];
                      }
                      
                      return (
                        <div className="gallery-card-video" onClick={() => openLightbox(item)}>
                          {thumbnailUrl ? (
                            <>
                              <img src={thumbnailUrl} alt={item.title} onError={(e) => {
                                // Fallback if thumbnail fails to load
                                e.target.style.display = 'none';
                                e.target.parentElement.innerHTML = '<div class="gallery-card-video-placeholder"><span style="font-size: 40px;">▶️</span><span>Video</span></div>';
                              }} />
                              <div className="gallery-card-overlay">
                                <Play size={24} />
                              </div>
                            </>
                          ) : item.video_file_url ? (
                            // For uploaded videos, generate thumbnail
                            <>
                              <VideoThumbnail
                                videoUrl={item.video_file_url}
                                title={item.title}
                                onThumbnailReady={(thumbUrl) => {
                                  setVideoThumbnails(prev => ({ ...prev, [item.id]: thumbUrl }));
                                }}
                              />
                              {videoThumbnails[item.id] ? (
                                <>
                                  <img src={videoThumbnails[item.id]} alt={item.title} />
                                  <div className="gallery-card-overlay">
                                    <Play size={24} />
                                  </div>
                                </>
                              ) : (
                                <div className="gallery-card-video-placeholder">
                                  <Play size={40} />
                                  <span>Loading...</span>
                                </div>
                              )}
                            </>
                          ) : (
                            <div className="gallery-card-video-placeholder">
                              <Play size={40} />
                              <span>Video</span>
                            </div>
                          )}
                        </div>
                      );
                    })()}
                    <div className="gallery-card-content">
                      <div className="gallery-card-badges">
                        <Badge variant="default" size="sm">
                          {eventTypes.find(t => t.value === item.event_type)?.label || item.event_type}
                        </Badge>
                      </div>
                      <h3 className="gallery-card-title">{item.title}</h3>
                      {item.event_date && (
                        <div className="gallery-card-meta">
                          <Calendar size={14} />
                          <span>{format(new Date(item.event_date), 'MMM d, yyyy')}</span>
                        </div>
                      )}
                    </div>
                  </Card>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Lightbox Modal */}
      {selectedItem && (
        <div className="gallery-lightbox" onClick={closeLightbox}>
          <div className="gallery-lightbox-content" onClick={(e) => e.stopPropagation()}>
            <button className="gallery-lightbox-close" onClick={closeLightbox} aria-label="Close">
              ×
            </button>
            {selectedItem.media_type === 'image' && selectedItem.image_url && (
              <div className="gallery-lightbox-image">
                <img src={selectedItem.image_url} alt={selectedItem.title} />
                <div className="gallery-lightbox-info">
                  <h3>{selectedItem.title}</h3>
                  {selectedItem.description && <p>{selectedItem.description}</p>}
                  {selectedItem.event_date && (
                    <div className="gallery-lightbox-meta">
                      <Calendar size={16} />
                      <span>{format(new Date(selectedItem.event_date), 'MMMM d, yyyy')}</span>
                    </div>
                  )}
                </div>
              </div>
            )}
            {selectedItem.media_type === 'video' && (
              <div className="gallery-lightbox-video">
                {selectedItem.embed_url ? (
                  <iframe
                    src={selectedItem.embed_url}
                    title={selectedItem.title}
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                  />
                ) : selectedItem.video_file_url ? (
                  <video controls autoPlay>
                    <source src={selectedItem.video_file_url} type="video/mp4" />
                    Your browser does not support the video tag.
                  </video>
                ) : (
                  <div className="gallery-lightbox-video-placeholder">
                    <Play size={64} />
                    <p>Video unavailable</p>
                  </div>
                )}
                <div className="gallery-lightbox-info">
                  <h3>{selectedItem.title}</h3>
                  {selectedItem.description && <p>{selectedItem.description}</p>}
                  {selectedItem.event_date && (
                    <div className="gallery-lightbox-meta">
                      <Calendar size={16} />
                      <span>{format(new Date(selectedItem.event_date), 'MMMM d, yyyy')}</span>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
      </div>
    </PageErrorBoundary>
  );
}

