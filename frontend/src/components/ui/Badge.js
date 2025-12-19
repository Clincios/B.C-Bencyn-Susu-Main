import React from 'react';
import './Badge.css';

const Badge = ({ 
  children, 
  className = '',
  variant = 'default',
  ...props 
}) => {
  return (
    <span
      className={`ui-badge ui-badge-${variant} ${className}`}
      {...props}
    >
      {children}
    </span>
  );
};

export default Badge;
