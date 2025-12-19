import React from 'react';

// Extended icon components for Updates page
export const Bell = ({ className = '', size = 16 }) => (
  <span className={className} style={{ fontSize: `${size}px` }}>🔔</span>
);

export const AlertCircle = ({ className = '', size = 16 }) => (
  <span className={className} style={{ fontSize: `${size}px` }}>⚠️</span>
);

export const Newspaper = ({ className = '', size = 16 }) => (
  <span className={className} style={{ fontSize: `${size}px` }}>📰</span>
);

export const CalendarIcon = ({ className = '', size = 16 }) => (
  <span className={className} style={{ fontSize: `${size}px` }}>📅</span>
);
