import React from 'react';

// Simple icon components using Unicode/Emoji
export const Calendar = ({ className = '', size = 16 }) => (
  <span className={className} style={{ fontSize: `${size}px` }}>📅</span>
);

export const User = ({ className = '', size = 16 }) => (
  <span className={className} style={{ fontSize: `${size}px` }}>👤</span>
);

export const ArrowRight = ({ className = '', size = 16 }) => (
  <span className={className} style={{ fontSize: `${size}px` }}>→</span>
);

export const Search = ({ className = '', size = 16 }) => (
  <span className={className} style={{ fontSize: `${size}px` }}>🔍</span>
);

export const Image = ({ className = '', size = 16 }) => (
  <span className={className} style={{ fontSize: `${size}px` }}>🖼️</span>
);

export const Play = ({ className = '', size = 16 }) => (
  <span className={className} style={{ fontSize: `${size}px` }}>▶️</span>
);