import React from 'react';
import './Input.css';

const Input = ({ 
  className = '', 
  ...props 
}) => {
  return (
    <input
      className={`ui-input ${className}`}
      {...props}
    />
  );
};

export default Input;
